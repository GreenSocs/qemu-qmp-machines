
.section .text
_start:
// put dtb address in x0
ldr x0, dtb
mov x1, xzr
mov x2, xzr
mov x3, xzr
// jump to entry point
ldr x4, entry
br x4

dtb:
.word 0x44000000 // LSB
.word 0x00000000 // MSB

entry:
.word 0x40200000 // LSB
.word 0x00000000 // MSB
