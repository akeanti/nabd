#include "esp_app_desc.h"
#include "esp_log.h"
#include "hardware_tier.h"

namespace {

constexpr char kLogTag[] = "nabd";

}  // namespace

extern "C" void app_main() {
  ESP_LOGI(kLogTag, "firmware %s, hardware tier %s", esp_app_get_description()->version,
           nabd::kHardwareTierName);
}
