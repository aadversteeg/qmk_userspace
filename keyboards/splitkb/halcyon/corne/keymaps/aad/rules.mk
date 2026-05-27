# This adds module functionality to your keyboard (files found in users/halcyon_modules)
USER_NAME := halcyon_modules

# Disable per-key RGB matrix — LEDs stay off (Halcyon module code is #ifdef-guarded, safe)
RGB_MATRIX_ENABLE = no

# One-handed QK_BOOT combos (defined in keymap.c) so each half can self-flash.
COMBO_ENABLE = yes
