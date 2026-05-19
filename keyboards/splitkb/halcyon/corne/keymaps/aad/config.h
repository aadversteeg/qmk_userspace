#pragma once

// ---------------------------------------------------------------------------
// Tap-hold tuning for the home-row mods (A/S/F · J/L/;) and the thumb
// layer-/mod-taps. QMK defaults are what make home-row mods feel flaky;
// this block is the single biggest improvement to daily typing feel.
// ---------------------------------------------------------------------------

// How long a dual-role key must be held before a bare hold counts as "hold".
#define TAPPING_TERM 200

// If another key is pressed AND released while a dual-role key is still held
// (an opposite-hand roll), resolve the dual-role key as HOLD. Makes the
// intended modifier/layer fire reliably during fast typing.
#define PERMISSIVE_HOLD

// Holding a dual-role key immediately after tapping it = HOLD, not an
// auto-repeat of the tapped letter. Stops stray letters when you tap a
// home-row key and then hold it as a modifier.
#define QUICK_TAP_TERM 0
