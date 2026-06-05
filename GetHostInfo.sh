#!/bin/bash

echo "========================================"
echo "           计算机系统硬件信息           "
echo "========================================"

# 1. 查询计算机名
HOSTNAME=$(uname -n)
echo "计算机名称:  $HOSTNAME"

# 2. 查询 CPU 核心数
# lscpu 或 /proc/cpuinfo 都可以，这里取逻辑核心数 (包括超线程)
CPU_CORES=$(nproc)
CPU_MODEL=$(grep 'model name' /proc/cpuinfo | head -n 1 | cut -d: -f2 | sed 's/^[ \t]*//')
echo "CPU 型号:    $CPU_MODEL"
echo "CPU 核心数:  $CPU_CORES 核"

# 3. 查询内存大小
# free -h 可以直接看到易读的格式（G或M）
MEM_TOTAL=$(free -h | awk '/^Mem:/ {print $2}')
MEM_AVAILABLE=$(free -h | awk '/^Mem:/ {print $7}')
echo "总内存大小:  $MEM_TOTAL (可用: $MEM_AVAILABLE)"

# 4. 查询硬盘大小
# df -h 统计挂载盘的总总量，或者用 lsblk 查看物理磁盘
echo "----------------------------------------"
echo "硬盘使用情况 (lsblk):"
lsblk -d -o NAME,SIZE,TYPE | grep disk

echo "----------------------------------------"
echo "分区挂载与空间 (df -h):"
df -h --total | grep -E 'Filesystem|total'
echo "========================================"
