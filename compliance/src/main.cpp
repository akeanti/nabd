#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string_view>

namespace {

constexpr std::string_view kReport =
    "# IEEE C37.118.1 P-class compliance report\n"
    "\n"
    "No test conditions are registered.\n";

}  // namespace

int main(int argc, char** argv) {
  if (argc != 3 || std::string_view(argv[1]) != "--report") {
    std::cerr << "usage: nabd_compliance --report <path>\n";
    return EXIT_FAILURE;
  }
  std::ofstream report(argv[2]);
  report << kReport;
  return report ? EXIT_SUCCESS : EXIT_FAILURE;
}
