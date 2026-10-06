#include <cstdlib>
#include <iostream>
#include <string_view>

namespace {

constexpr std::string_view kReport =
    "# IEEE C37.118.1 P-class compliance report\n"
    "\n"
    "No test conditions are registered.\n";

}  // namespace

int main() {
  std::cout << kReport;
  return std::cout ? EXIT_SUCCESS : EXIT_FAILURE;
}
