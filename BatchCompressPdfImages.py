import os
import shutil
import subprocess
import argparse
from pathlib import Path

#!/usr/bin/env python3
"""
批量压缩 PDF（调用 Ghostscript），保持目录结构并尽量让文件大小减小到原来的一半。
依赖：系统安装 Ghostscript（可执行名 gs 或 gswin64c/gswin32c）。
"""


def find_gs():
    for name in ("gs", "gswin64c", "gswin32c"):
        p = shutil.which(name)
        if p:
            return p
    return None

def compress_with_gs(gs_cmd, src_path, dst_path, dpi):
    # 使用 pdfwrite 并设置图片 downsample 分辨率
    cmd = [
        gs_cmd,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dNOPAUSE",
        "-dBATCH",
        "-dQUIET",
        # 启用图片 downsample（按 DPI 降采样）
        "-dDownsampleColorImages=true",
        "-dDownsampleGrayImages=true",
        "-dDownsampleMonoImages=true",
        f"-dColorImageDownsampleType=/Bicubic",
        f"-dColorImageResolution={dpi}",
        f"-dGrayImageDownsampleType=/Bicubic",
        f"-dGrayImageResolution={dpi}",
        f"-dMonoImageDownsampleType=/Subsample",
        f"-dMonoImageResolution={dpi}",
        # 强制使用更高效的编码（JPEG）以进一步减小文件体积
        "-dAutoFilterColorImages=true",
        "-dAutoFilterGrayImages=true",
        "-dAutoFilterMonoImages=true",
        "-dColorImageFilter=/DCTEncode",
        "-dGrayImageFilter=/DCTEncode",
        # JPEG 质量（可根据需要调整，范围约 0-100）
        "-dJPEGQ=60",
        # 输出与输入
        "-sOutputFile=" + str(dst_path),
        str(src_path),
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res.returncode == 0

def ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

def process_file(gs_cmd, src_file: Path, dst_file: Path, target_ratio=0.5, dpi_list=(150,120,96,72)):
    ensure_parent(dst_file)
    orig_size = src_file.stat().st_size
    # 如果目标已存在且满足要求则跳过
    if dst_file.exists() and dst_file.stat().st_size <= orig_size * target_ratio:
        print(f"跳过（已满足目标）：{src_file}")
        return

    tmp = dst_file.with_suffix(dst_file.suffix + ".tmp")
    for dpi in dpi_list:
        success = compress_with_gs(gs_cmd, src_file, tmp, dpi)
        if not success:
            print(f"Ghostscript 处理失败: {src_file} (dpi={dpi})")
            if tmp.exists():
                tmp.unlink()
            return
        new_size = tmp.stat().st_size
        ratio = new_size / orig_size
        print(f"{src_file} -> dpi={dpi}, size {orig_size} -> {new_size} ({ratio:.2%})")
        # 如果达标或已到最低档则保存结果
        if ratio <= target_ratio or dpi == dpi_list[-1]:
            # 覆盖目标文件
            tmp.replace(dst_file)
            return
        # 否则继续使用更低分辨率尝试
    # 如果循环结束但未保存（理论上不会），则删除临时文件
    if tmp.exists():
        tmp.unlink()

def walk_and_process(gs_cmd, src_root: Path, dst_root: Path, target_ratio=0.5, dpi_list=(150,120,96,72)):
    for root, dirs, files in os.walk(src_root):
        for name in files:
            if not name.lower().endswith(".pdf"):
                continue
            src_file = Path(root) / name
            rel = src_file.relative_to(src_root)
            dst_file = dst_root / rel
            process_file(gs_cmd, src_file, dst_file, target_ratio, dpi_list)

def main():
    parser = argparse.ArgumentParser(description="批量压缩 PDF（基于 Ghostscript），保持目录结构")
    parser.add_argument("--src", default=str(Path.cwd()), help="源目录，例如 D:\\Downloads\\00-CATL\\CBESS\\PunchList\\old；默认为当前目录")
    parser.add_argument("--dst", default=None, help="目标目录，例如 D:\\Downloads\\00-CATL\\CBESS\\PunchList\\Compressed；默认为 <src>/Compressed")
    parser.add_argument("--ratio", type=float, default=0.5, help="目标大小比例（默认 0.5，即 50%）")
    parser.add_argument("--dpis", nargs="*", type=int, default=[150,120,96,72], help="尝试的 DPI 列表，越后面越低")
    args = parser.parse_args()
    if args.dst is None:
        args.dst = str(Path(args.src).resolve() / "Compressed")

    gs_cmd = find_gs()
    if not gs_cmd:
        print("找不到 Ghostscript 可执行文件。请安装 Ghostscript 并确保 gs 或 gswin64c 在 PATH 中。")
        return

    src_root = Path(args.src).resolve()
    dst_root = Path(args.dst).resolve()
    if not src_root.exists():
        print("源目录不存在:", src_root)
        return
    dst_root.mkdir(parents=True, exist_ok=True)

    walk_and_process(gs_cmd, src_root, dst_root, args.ratio, tuple(args.dpis))
    print("处理完成。")

if __name__ == "__main__":
    main()