#!/usr/bin/env python3
import argparse
import math


def positive_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("value must be a finite positive number")
    return number


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estimate a C500 Roofline point from explicit FLOPs and bytes."
    )
    parser.add_argument("--flops", type=positive_float, required=True)
    parser.add_argument("--bytes", type=positive_float, required=True)
    parser.add_argument("--bandwidth-gbps", type=positive_float, required=True)
    parser.add_argument("--compute-tflops", type=positive_float, required=True)
    parser.add_argument("--time-ms", type=positive_float)
    args = parser.parse_args()

    arithmetic_intensity = args.flops / args.bytes
    ridge = args.compute_tflops * 1000.0 / args.bandwidth_gbps
    memory_roof = arithmetic_intensity * args.bandwidth_gbps / 1000.0
    attainable = min(args.compute_tflops, memory_roof)
    theoretical_bound = "memory" if arithmetic_intensity < ridge else "compute"

    print(f"arithmetic_intensity_flop_per_byte={arithmetic_intensity:.6f}")
    print(f"ridge_point_flop_per_byte={ridge:.6f}")
    print(f"memory_roof_tflops={memory_roof:.6f}")
    print(f"compute_roof_tflops={args.compute_tflops:.6f}")
    print(f"attainable_roof_tflops={attainable:.6f}")
    print(f"theoretical_bound={theoretical_bound}")

    if args.time_ms is not None:
        achieved_tflops = args.flops / (args.time_ms * 1.0e9)
        effective_bandwidth = args.bytes / (args.time_ms * 1.0e6)
        roof_efficiency = achieved_tflops / attainable
        compute_efficiency = achieved_tflops / args.compute_tflops
        bandwidth_efficiency = effective_bandwidth / args.bandwidth_gbps
        print(f"achieved_tflops={achieved_tflops:.6f}")
        print(f"effective_bandwidth_gbps={effective_bandwidth:.6f}")
        print(f"attainable_roof_efficiency={roof_efficiency:.6%}")
        print(f"compute_roof_efficiency={compute_efficiency:.6%}")
        print(f"bandwidth_roof_efficiency={bandwidth_efficiency:.6%}")


if __name__ == "__main__":
    main()

