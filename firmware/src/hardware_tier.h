#pragma once

namespace nabd {

#if defined(NABD_TIER_A) == defined(NABD_TIER_B)
#error "Define exactly one of NABD_TIER_A or NABD_TIER_B"
#endif

enum class HardwareTier { kA, kB };

#if defined(NABD_TIER_A)
inline constexpr HardwareTier kHardwareTier = HardwareTier::kA;
inline constexpr char kHardwareTierName[] = "A";
#else
inline constexpr HardwareTier kHardwareTier = HardwareTier::kB;
inline constexpr char kHardwareTierName[] = "B";
#endif

}  // namespace nabd
