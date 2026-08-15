# $processList = @(
    # "msedgewebview2",
    # "WeChatAppEx"
# )

# foreach ($procName in $processList) {
    # Stop-Process -Name $procName -Force -ErrorAction SilentlyContinue
# }

<#
.SYNOPSIS
    一键强制清理所有进程的工作集内存，将系统内存占用降至最低。
    注意：请以管理员身份运行 PowerShell 执行此脚本！
#>

# 1. 动态加载 Windows API
$SetProcessWorkingSetSize = Add-Type -MemberDefinition @"
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool SetProcessWorkingSetSize(IntPtr hProcess, IntPtr dwMinimumWorkingSetSize, IntPtr dwMaximumWorkingSetSize);
    [DllImport("psapi.dll")]
    public static extern bool EmptyWorkingSet(IntPtr hProcess);
"@ -Name "Win32Memory" -Namespace "Win32Utils" -PassThru

# 2. 尝试提升当前脚本权限以处理系统级进程
[System.Diagnostics.Process]::GetCurrentProcess().PriorityClass = [System.Diagnostics.ProcessPriorityClass]::High

Write-Host "开始清理进程内存工作集..." -ForegroundColor Green

# 3. 获取所有进程并清理
$processes = Get-Process
$successCount = 0

foreach ($proc in $processes) {
    try {
        # 排除已经退出或无效的句柄
        if (-not $proc.HasExited -and $proc.Handle -ne [IntPtr]::Zero) {
            # 方式1：使用 EmptyWorkingSet 强制清空该进程的 WorkingSet
            $null = [Win32Utils.Win32Memory]::EmptyWorkingSet($proc.Handle)
            $successCount++
        }
    }
    catch {
        # 部分系统核心进程（如 Idle, System, 权限不足的进程）会被忽略，属于正常现象
        continue
    }
}

# 4. 强制触发 .NET 垃圾回收（清理 PowerShell 本身）
[GC]::Collect()
[GC]::WaitForPendingFinalizers()

Write-Host "清理完成！成功处理了 $successCount 个进程。" -ForegroundColor Cyan
Write-Host "请打开任务管理器观察当前的内存占用。" -ForegroundColor Yellow