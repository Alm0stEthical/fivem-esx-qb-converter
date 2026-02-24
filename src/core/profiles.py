import re
from pathlib import Path

PROFILE_GENERIC = "Generic"
PROFILE_QB_BANKING_ESX_COMPAT = "QB-Core -> ESX (Compat Bridge)"

PROFILES = [
    PROFILE_GENERIC,
    PROFILE_QB_BANKING_ESX_COMPAT,
]

CLIENT_COMPAT_MARKER = "-- ESX_COMPAT_QB_BANKING_CLIENT"
SERVER_COMPAT_MARKER = "-- ESX_COMPAT_QB_BANKING_SERVER"

CLIENT_COMPAT_BLOCK = """-- ESX_COMPAT_QB_BANKING_CLIENT
local ESX = exports['es_extended']:getSharedObject()

local function ShowPromptCompat(text)
    if GetResourceState('ox_lib') == 'started' then
        exports.ox_lib:showTextUI(text)
        return
    end
    if ESX and ESX.ShowHelpNotification then
        ESX.ShowHelpNotification(text)
    end
end

local function HidePromptCompat()
    if GetResourceState('ox_lib') == 'started' then
        exports.ox_lib:hideTextUI()
    end
end

local function getTargetResource()
    if GetResourceState('qb-target') == 'started' then
        return 'qb-target'
    end
    if GetResourceState('qtarget') == 'started' then
        return 'qtarget'
    end
    return nil
end

local function AddCircleZoneCompat(name, coords, radius, zoneOptions, targetData)
    local resource = getTargetResource()
    if resource then
        return exports[resource]:AddCircleZone(name, coords, radius, zoneOptions, targetData)
    end
    if GetResourceState('ox_target') == 'started' then
        local options = {}
        for _, opt in ipairs(targetData.options or {}) do
            options[#options + 1] = {
                name = opt.name or name,
                icon = opt.icon,
                label = opt.label,
                item = opt.item,
                onSelect = opt.action,
            }
        end
        return exports.ox_target:addSphereZone({
            coords = coords,
            radius = radius,
            debug = zoneOptions and zoneOptions.debugPoly or false,
            options = options,
        })
    end
end

local function AddTargetModelCompat(model, targetData)
    local resource = getTargetResource()
    if resource then
        return exports[resource]:AddTargetModel(model, targetData)
    end
    if GetResourceState('ox_target') == 'started' then
        local options = {}
        for _, opt in ipairs(targetData.options or {}) do
            options[#options + 1] = {
                name = opt.name or tostring(model),
                icon = opt.icon,
                label = opt.label,
                item = opt.item,
                onSelect = opt.action,
            }
        end
        return exports.ox_target:addModel(model, options)
    end
end

local QBCore = {}
QBCore.Functions = {}

QBCore.Functions.TriggerCallback = function(name, cb, ...)
    ESX.TriggerServerCallback(name, cb, ...)
end

QBCore.Functions.Notify = function(message, _)
    if ESX and ESX.ShowNotification then
        ESX.ShowNotification(message)
    end
end

QBCore.Functions.Progressbar = function(_, _, duration, _, _, _, _, _, onFinish, _)
    local waitMs = tonumber(duration) or 0
    SetTimeout(waitMs, function()
        if onFinish then
            onFinish()
        end
    end)
end

RegisterNetEvent('QBCore:Notify', function(message, _, _)
    if ESX and ESX.ShowNotification then
        ESX.ShowNotification(message)
    end
end)
"""

SERVER_COMPAT_BLOCK = """-- ESX_COMPAT_QB_BANKING_SERVER
local ESX = exports['es_extended']:getSharedObject()

local function GetFrameworkJobsCompat()
    if ESX.GetJobs then
        return ESX.GetJobs()
    end
    return ESX.Jobs or {}
end

local function GetCashMoneyCompat(xPlayer)
    if xPlayer.getMoney then
        return xPlayer.getMoney()
    end
    local account = xPlayer.getAccount and xPlayer.getAccount('money')
    return account and account.money or 0
end

local function GetBankMoneyCompat(xPlayer)
    local account = xPlayer.getAccount and xPlayer.getAccount('bank')
    return account and account.money or 0
end

local function NormalizeMoneyTypeCompat(moneyType)
    if moneyType == 'cash' then
        return 'money'
    end
    return moneyType
end

local function AddItemCompat(source, itemName, amount, ...)
    local count = tonumber(amount) or 1
    local args = { ... }
    local info = {}
    for _, value in ipairs(args) do
        if type(value) == 'table' then
            info = value
            break
        end
    end

    if GetResourceState('ox_inventory') == 'started' then
        local ok = exports.ox_inventory:AddItem(source, itemName, count, info or {})
        return ok ~= false and ok ~= nil
    end
    if GetResourceState('qb-inventory') == 'started' then
        local ok = exports['qb-inventory']:AddItem(
            source,
            itemName,
            count,
            false,
            info or {},
            'banking:compat'
        )
        return ok ~= false and ok ~= nil
    end
    local xPlayer = ESX.GetPlayerFromId(source)
    if not xPlayer or not xPlayer.addInventoryItem then
        return false
    end
    xPlayer.addInventoryItem(itemName, count)
    return true
end

local function GetItemsByNameCompat(source, itemName)
    if GetResourceState('qb-inventory') == 'started' then
        return exports['qb-inventory']:GetItemsByName(source, itemName)
    end
    if GetResourceState('ox_inventory') == 'started' then
        local slots = exports.ox_inventory:Search(source, 'slots', itemName)
        if type(slots) ~= 'table' then
            return nil
        end
        local out = {}
        for _, slot in pairs(slots) do
            out[#out + 1] = {
                name = itemName,
                info = slot.metadata or {},
            }
        end
        if #out > 0 then
            return out
        end
        return nil
    end
    local xPlayer = ESX.GetPlayerFromId(source)
    if not xPlayer or not xPlayer.getInventoryItem then
        return nil
    end
    local item = xPlayer.getInventoryItem(itemName)
    if item and (item.count or 0) > 0 then
        local out = {}
        for _ = 1, item.count do
            out[#out + 1] = { name = itemName, info = {} }
        end
        return out
    end
    return nil
end

local function BuildPlayerDataCompat(xPlayer)
    local job = xPlayer.getJob and xPlayer.getJob() or {}
    local gradeLevel = tonumber(job.grade) or tonumber(job.grade_level) or 0
    local gradeName = job.grade_name or ''
    local isBoss = gradeName == 'boss' or gradeLevel >= 4

    local firstname = ''
    local lastname = ''
    if xPlayer.get then
        firstname = xPlayer.get('firstName') or xPlayer.get('firstname') or ''
        lastname = xPlayer.get('lastName') or xPlayer.get('lastname') or ''
    end

    local gangData = { name = 'none', label = 'None', grade = { level = 0, name = 'none' }, isboss = false }
    if xPlayer.get then
        local gang = xPlayer.get('gang')
        if type(gang) == 'table' then
            local gangGrade = gang.grade or {}
            gangData = {
                name = gang.name or 'none',
                label = gang.label or gang.name or 'None',
                grade = {
                    level = tonumber(gangGrade.level or gangGrade.grade) or 0,
                    name = gangGrade.name or '',
                },
                isboss = gang.isboss == true,
            }
        end
    end

    return {
        source = xPlayer.source,
        citizenid = xPlayer.identifier,
        charinfo = {
            firstname = firstname,
            lastname = lastname,
        },
        money = {
            cash = GetCashMoneyCompat(xPlayer),
            bank = GetBankMoneyCompat(xPlayer),
        },
        job = {
            name = job.name or 'unemployed',
            label = job.label or job.name or 'Unemployed',
            grade = {
                level = gradeLevel,
                name = gradeName,
            },
            isboss = isBoss,
        },
        gang = gangData,
    }
end

local function WrapPlayerCompat(xPlayer)
    if not xPlayer then
        return nil
    end

    local wrapped = {}
    wrapped.PlayerData = BuildPlayerDataCompat(xPlayer)
    wrapped.Functions = {}

    wrapped.Functions.GetMoney = function(_, moneyType)
        local kind = NormalizeMoneyTypeCompat(moneyType)
        if kind == 'money' then
            return GetCashMoneyCompat(xPlayer)
        end
        local account = xPlayer.getAccount and xPlayer.getAccount(kind)
        return account and account.money or 0
    end

    wrapped.Functions.AddMoney = function(_, moneyType, amount, _)
        local kind = NormalizeMoneyTypeCompat(moneyType)
        local amt = tonumber(amount) or 0
        if kind == 'money' then
            if xPlayer.addMoney then
                xPlayer.addMoney(amt)
            end
        elseif xPlayer.addAccountMoney then
            xPlayer.addAccountMoney(kind, amt)
        end
        wrapped.PlayerData = BuildPlayerDataCompat(xPlayer)
        return true
    end

    wrapped.Functions.RemoveMoney = function(_, moneyType, amount, _)
        local kind = NormalizeMoneyTypeCompat(moneyType)
        local amt = tonumber(amount) or 0
        if kind == 'money' then
            if xPlayer.removeMoney then
                xPlayer.removeMoney(amt)
            end
        elseif xPlayer.removeAccountMoney then
            xPlayer.removeAccountMoney(kind, amt)
        end
        wrapped.PlayerData = BuildPlayerDataCompat(xPlayer)
        return true
    end

    wrapped.Functions.AddItem = function(_, itemName, amount, _, info, _)
        local ok = AddItemCompat(xPlayer.source, itemName, amount, info)
        wrapped.PlayerData = BuildPlayerDataCompat(xPlayer)
        return ok
    end

    wrapped.Functions.GetItemsByName = function(_, itemName)
        return GetItemsByNameCompat(xPlayer.source, itemName)
    end

    wrapped.Functions.GetItemByName = function(_, itemName)
        local items = GetItemsByNameCompat(xPlayer.source, itemName)
        if items and items[1] then
            return items[1]
        end
        return nil
    end

    return wrapped
end

local function GetPlayerByIdentifierCompat(identifier)
    for _, source in ipairs(ESX.GetPlayers()) do
        local xPlayer = ESX.GetPlayerFromId(source)
        if xPlayer and tostring(xPlayer.identifier) == tostring(identifier) then
            return xPlayer
        end
    end
    return nil
end

local QBCore = {}
QBCore.Functions = {}
QBCore.Commands = {}
QBCore.Shared = {}
QBCore.Shared.Jobs = GetFrameworkJobsCompat()

QBCore.Functions.GetPlayer = function(playerId)
    return WrapPlayerCompat(ESX.GetPlayerFromId(playerId))
end

QBCore.Functions.GetPlayerByCitizenId = function(citizenid)
    return WrapPlayerCompat(GetPlayerByIdentifierCompat(citizenid))
end

QBCore.Functions.GetPlayers = function()
    return ESX.GetPlayers()
end

QBCore.Functions.CreateCallback = function(name, callback)
    ESX.RegisterServerCallback(name, function(source, cb, ...)
        callback(source, cb, ...)
    end)
end

QBCore.Functions.CreateUseableItem = function(itemName, callback)
    ESX.RegisterUsableItem(itemName, function(source)
        callback(source, { name = itemName })
    end)
end

QBCore.Commands.Add = function(name, _, _, _, callback)
    RegisterCommand(name, function(source, args, raw)
        callback(source, args, raw)
    end, false)
end

local function LogCompat(...)
    if GetResourceState('qb-log') == 'started' then
        TriggerEvent('qb-log:server:CreateLog', ...)
        return
    end
    local args = { ... }
    print(('[compat_bridge][log] %s'):format(table.concat(args, ' | ')))
end
"""

LOCALE_COMPAT = """Locale = Locale or {}
Locale.__index = Locale

function Locale:new(data)
    local obj = setmetatable({}, self)
    obj.phrases = (data and data.phrases) or {}
    obj.warnOnMissing = (data and data.warnOnMissing) or false
    return obj
end

local function locale_lookup(tbl, key)
    local current = tbl
    for part in string.gmatch(key or '', '([^%.]+)') do
        if type(current) ~= 'table' then
            return nil
        end
        current = current[part]
    end
    return current
end

function Locale:t(key)
    local value = locale_lookup(self.phrases, key)
    if value ~= nil then
        return value
    end
    if self.warnOnMissing then
        print(('[locale_compat] missing phrase: %s'):format(tostring(key)))
    end
    return tostring(key)
end
"""


def _remove_framework_bootstrap(content: str) -> str:
    content = re.sub(
        r"^\s*local\s+QBCore\s*=\s*exports\[['\"]qb-core['\"]\]:GetCoreObject\(\)\s*\n?",
        "",
        content,
        flags=re.MULTILINE,
    )
    content = re.sub(
        r"^\s*QBCore\s*=\s*exports\[['\"]qb-core['\"]\]:GetCoreObject\(\)\s*\n?",
        "",
        content,
        flags=re.MULTILINE,
    )
    content = re.sub(
        r"^\s*local\s+ESX\s*=\s*exports\[['\"]es_extended['\"]\]:getSharedObject\(\)\s*\n?",
        "",
        content,
        flags=re.MULTILINE,
    )
    return content.lstrip()


def _is_manifest_file(path: str) -> bool:
    return path.endswith("fxmanifest.lua") or path.endswith("__resource.lua")


def _role_scores(path: str, content: str) -> tuple[int, int]:
    lower = content.lower()
    normalized = path.replace("\\", "/").lower()

    client_score = 0
    server_score = 0

    if "/client" in normalized or normalized.startswith("client"):
        client_score += 3
    if "/server" in normalized or normalized.startswith("server"):
        server_score += 3

    client_hints = [
        "registernuicallback(",
        "setnuifocus(",
        "sendnuimessage(",
        "playerpedid(",
        "getentitycoords(playerpedid())",
        "addblipforcoord(",
        "qbcore.functions.progressbar",
        "exports['qb-target']",
        'exports["qb-target"]',
        "exports['qtarget']",
        'exports["qtarget"]',
        "drawtext(",
        "hidetext()",
        "combozone:create(",
        "circlezone:create(",
    ]

    server_hints = [
        "qbcore.functions.createcallback(",
        "qbcore.functions.createuseableitem(",
        "qbcore.commands.add(",
        "mysql.",
        "registercommand(",
        "registerserverevent(",
        "triggerclientevent(",
        "exports['qb-inventory']",
        'exports["qb-inventory"]',
        "exports(",
    ]

    for hint in client_hints:
        if hint in lower:
            client_score += 1
    for hint in server_hints:
        if hint in lower:
            server_score += 1

    return client_score, server_score


def _rewrite_client_qb_banking(content: str) -> str:
    content = _remove_framework_bootstrap(content)
    content = content.replace("exports['qb-core']:DrawText(", "ShowPromptCompat(")
    content = content.replace('exports["qb-core"]:DrawText(', "ShowPromptCompat(")
    content = content.replace("exports['qb-core']:HideText()", "HidePromptCompat()")
    content = content.replace('exports["qb-core"]:HideText()', "HidePromptCompat()")
    content = content.replace("exports['qb-target']:AddCircleZone(", "AddCircleZoneCompat(")
    content = content.replace("exports['qtarget']:AddCircleZone(", "AddCircleZoneCompat(")
    content = content.replace("exports['qb-target']:AddTargetModel(", "AddTargetModelCompat(")
    content = content.replace("exports['qtarget']:AddTargetModel(", "AddTargetModelCompat(")
    if CLIENT_COMPAT_MARKER not in content:
        content = f"{CLIENT_COMPAT_BLOCK}\n\n{content}"
    return content


def _rewrite_server_qb_banking(content: str) -> str:
    content = _remove_framework_bootstrap(content)
    content = re.sub(
        r"exports\[['\"]qb-inventory['\"]\]:AddItem\(",
        "AddItemCompat(",
        content,
    )
    content = re.sub(
        r"TriggerEvent\('qb-log:server:CreateLog',\s*([^\n]+)\)",
        r"LogCompat(\1)",
        content,
    )
    if SERVER_COMPAT_MARKER not in content:
        content = f"{SERVER_COMPAT_BLOCK}\n\n{content}"
    return content


def _rewrite_fxmanifest_qb_banking(content: str) -> str:
    lines = content.splitlines()
    out: list[str] = []
    inserted_locale = False

    for line in lines:
        if "@qb-core/shared/locale.lua" in line:
            if not inserted_locale:
                out.append("    'locale_compat.lua',")
                inserted_locale = True
            continue
        out.append(line)

    if not inserted_locale:
        for idx, line in enumerate(out):
            if line.strip().startswith("shared_scripts"):
                out.insert(idx + 1, "    'locale_compat.lua',")
                inserted_locale = True
                break

    return "\n".join(out) + ("\n" if content.endswith("\n") else "")


def apply_profile_rewrite(
    content: str,
    relative_path: str,
    direction: str,
    profile: str,
) -> str:
    if profile != PROFILE_QB_BANKING_ESX_COMPAT or direction != "QB-Core to ESX":
        return content

    path = relative_path.replace("\\", "/").lower()
    if _is_manifest_file(path):
        return _rewrite_fxmanifest_qb_banking(content)

    if not path.endswith(".lua"):
        return content

    lowered = content.lower()
    if (
        "qbcore" not in lowered
        and "qb-core" not in lowered
        and "qb-target" not in lowered
        and "qtarget" not in lowered
    ):
        return content

    client_score, server_score = _role_scores(path, content)
    if server_score > client_score:
        return _rewrite_server_qb_banking(content)
    return _rewrite_client_qb_banking(content)

    return content


def write_profile_extras(destination_root: Path, direction: str, profile: str) -> list[Path]:
    created: list[Path] = []
    if profile == PROFILE_QB_BANKING_ESX_COMPAT and direction == "QB-Core to ESX":
        compat_path = destination_root / "locale_compat.lua"
        compat_path.write_text(LOCALE_COMPAT, encoding="utf-8")
        created.append(compat_path)
    return created
