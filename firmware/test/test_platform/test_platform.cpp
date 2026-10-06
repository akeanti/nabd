#include <unity.h>

#include <cstdint>
#include <cstring>
#include <limits>

void setUp() {}
void tearDown() {}

namespace {

void test_floating_point_types_are_ieee754() {
  TEST_ASSERT_TRUE(std::numeric_limits<float>::is_iec559);
  TEST_ASSERT_TRUE(std::numeric_limits<double>::is_iec559);
}

void test_float_has_ieee754_binary32_layout() {
  // IEEE 754 binary32 encodes 1.0 as 0x3F800000; C37.118.2 floating-point fields use binary32.
  const float one = 1.0f;
  std::uint32_t bits = 0;
  std::memcpy(&bits, &one, sizeof bits);
  TEST_ASSERT_EQUAL_HEX32(0x3F800000u, bits);
}

}  // namespace

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_floating_point_types_are_ieee754);
  RUN_TEST(test_float_has_ieee754_binary32_layout);
  return UNITY_END();
}
