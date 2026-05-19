#include QMK_KEYBOARD_H

// aad — Halcyon Corne rev2.
// C port of the former keymap.json (functionally identical), so it can carry
// config.h tap-hold tuning. Ported from a 34-key Ferris/Sweep layout.
// Tap dances intentionally omitted. Module row + (absent) encoders are plain
// keys here since this builds with HLC_NONE (no module).

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {

    // Layer 0 — Base (QWERTY, home-row mods A/S/F · J/L/;)
    [0] = LAYOUT_corne_hlc(
        KC_ESC,  KC_Q,              KC_W,              KC_E,    KC_R,              KC_T,         KC_Y,    KC_U,               KC_I,    KC_O,               KC_P,                  KC_BSPC,
        KC_LSFT, MT(MOD_LGUI,KC_A), MT(MOD_LALT,KC_S), KC_D,    MT(MOD_LCTL,KC_F), KC_G,         KC_H,    MT(MOD_RCTL,KC_J),  KC_K,    MT(MOD_LALT,KC_L),  MT(MOD_RGUI,KC_SCLN),  KC_QUOT,
        KC_LCTL, KC_Z,              KC_X,              KC_C,    KC_V,              KC_B,         KC_N,    KC_M,               KC_COMM, KC_DOT,             KC_SLSH,               KC_ENT,
                                          KC_LGUI, LT(1,KC_TAB), MT(MOD_LCTL,KC_ENT),     MT(MOD_RSFT,KC_SPC), LT(2,KC_BSPC), KC_RALT,
                  KC_MUTE, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,    KC_MUTE, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX
    ),

    // Layer 1 — Function / Navigation (hold left-inner thumb = Tab)
    [1] = LAYOUT_corne_hlc(
        _______, KC_F1,  KC_F2,                KC_F3,   KC_F4,                 KC_F5,        KC_F6,   KC_F7,                   KC_F8,   KC_F9,                  KC_F10,  _______,
        _______, KC_DEL, MT(MOD_LALT,KC_WBAK), KC_HOME, MT(MOD_LCTL,KC_LEFT),  KC_F11,       KC_F12,  MT(MOD_RCTL,KC_RIGHT),   KC_END,  MT(MOD_LALT,KC_WFWD),   KC_BSPC, _______,
        _______, KC_TAB, XXXXXXX,              XXXXXXX, KC_UP,                 KC_PGUP,      KC_PGDN, KC_DOWN,                 XXXXXXX, XXXXXXX,                KC_ESC,  _______,
                                          _______, XXXXXXX, _______,     _______, MO(3), _______,
                  _______, _______, _______, _______, _______,    _______, _______, _______, _______, _______
    ),

    // Layer 2 — Numbers / Symbols (hold right-inner thumb = Bspc)
    [2] = LAYOUT_corne_hlc(
        _______, KC_EXLM, KC_AT,   KC_HASH, KC_DLR,            KC_PERC,      KC_CIRC, KC_AMPR,            KC_ASTR, KC_BSLS, KC_GRV,  _______,
        _______, KC_1,    KC_2,    KC_3,    MT(MOD_LCTL,KC_4), KC_5,         KC_6,    MT(MOD_RCTL,KC_7),  KC_8,    KC_9,    KC_0,    _______,
        _______, KC_TILD, KC_UNDS, KC_PIPE, XXXXXXX,           XXXXXXX,      XXXXXXX, XXXXXXX,            KC_EQL,  KC_PLUS, KC_MINS, _______,
                                          _______, MO(3), _______,     _______, XXXXXXX, _______,
                  _______, _______, _______, _______, _______,    _______, _______, _______, _______, _______
    ),

    // Layer 3 — Brackets / Media (hold both inner thumbs)
    [3] = LAYOUT_corne_hlc(
        _______, LALT(LCTL(KC_DEL)), KC_LT,   KC_LBRC,        KC_LCBR, KC_LPRN,        KC_RPRN, KC_RCBR,  KC_RBRC,        KC_GT,   KC_CAPS, _______,
        _______, XXXXXXX,            XXXXXXX, LCTL(KC_MINS),  KC_WBAK, LSFT(KC_QUOT),  KC_QUOT, KC_WFWD,  LCTL(KC_EQL),   XXXXXXX, XXXXXXX, _______,
        _______, XXXXXXX,            XXXXXXX, XXXXXXX,        XXXXXXX, XXXXXXX,        XXXXXXX, XXXXXXX,  XXXXXXX,        XXXXXXX, MO(4),   _______,
                                          _______, XXXXXXX, XXXXXXX,     XXXXXXX, XXXXXXX, _______,
                  _______, _______, _______, _______, _______,    _______, _______, _______, _______, _______
    ),

    // Layer 4 — System (BOOT)
    [4] = LAYOUT_corne_hlc(
        _______, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,      XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, _______,
        _______, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,      XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, _______,
        _______, QK_BOOT, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,      XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, _______,
                                          _______, XXXXXXX, XXXXXXX,     XXXXXXX, XXXXXXX, _______,
                  _______, _______, _______, _______, _______,    _______, _______, _______, _______, _______
    )
};

// Snappy layers, precise home-row mods:
//  - Layer-tap thumb keys switch to the layer the instant another key is
//    pressed (no waiting on TAPPING_TERM).
//  - Mod-tap (home-row) keys do NOT, so fast same-hand rolls don't fire a
//    stray modifier; they rely on TAPPING_TERM + PERMISSIVE_HOLD instead.
bool get_hold_on_other_key_press(uint16_t keycode, keyrecord_t *record) {
    switch (keycode) {
        case QK_LAYER_TAP ... QK_LAYER_TAP_MAX:
            return true;
        default:
            return false;
    }
}
