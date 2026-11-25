"""A soft tanpura-style drone: Pa, Sa, Sa, low Sa, plucked in a slow cycle, with a sweeping overtone (jawari) and a light room."""
import numpy as np, wave, sys

SR = 48000


def drone(DUR, OUT, level_db=-20.0, seed=7):
    """write a stereo 48 kHz WAV of DUR seconds to OUT; quiet background level (RMS about level_db dBFS)"""
    rng = np.random.default_rng(seed)
    SA = 138.59  # C#3
    NOTES = [SA * 3 / 4, SA, SA, SA / 2]  # Pa, Sa, Sa, low Sa
    CYCLE, GAP = 5.2, 1.15
    N = int(SR * DUR)
    out = np.zeros((2, N))
    PL = 9.0  # seconds each pluck rings
    tt = np.arange(int(SR * PL)) / SR


    def pluck(f0, amp, detune):
        y = np.zeros_like(tt)
        centre = 2.0 + 15.0 * (1 - np.exp(-tt / 2.4))  # the overtone that sings, rising over the note
        for n in range(1, 31):
            fn = n * f0 * np.sqrt(1 + 0.00002 * n * n) * detune
            if fn > 9000:
                break
            bump = 1 + 2.2 * np.exp(-((n - centre) ** 2) / (2 * 2.0 ** 2))
            env = (1 - np.exp(-tt / 0.008)) * np.exp(-tt * (1 / 3.6 + 0.022 * n))
            y += (1 / n ** 1.15) * bump * env * np.sin(2 * np.pi * fn * tt + rng.uniform(0, 2 * np.pi))
        return amp * y


    t0 = 0.6
    while t0 < DUR:
        for k, f in enumerate(NOTES):
            start = t0 + k * GAP + rng.uniform(-0.03, 0.03)
            if start >= DUR:
                break
            i0 = int(start * SR)
            amp = (0.9 if k == 0 else 1.0 if k < 3 else 0.8) * rng.uniform(0.92, 1.05)
            for ch, det in ((0, 1.0), (1, 1.0007)):
                y = pluck(f, amp, det)
                i1 = min(N, i0 + len(y))
                out[ch, i0:i1] += y[: i1 - i0]
        t0 += CYCLE

    # gentle tone: roll off the top
    spec = np.fft.rfft(out, axis=1)
    fr = np.fft.rfftfreq(N, 1 / SR)
    spec *= 1 / np.sqrt(1 + (fr / 3200.0) ** 4)
    out = np.fft.irfft(spec, n=N, axis=1)

    # light room: decaying noise, a little different per side
    L = int(SR * 2.6)
    ir_t = np.arange(L) / SR
    wet = np.zeros_like(out)
    for ch in range(2):
        ir = rng.standard_normal(L) * np.exp(-ir_t / 0.75)
        ir[: int(0.012 * SR)] = 0
        ir /= np.sqrt(np.sum(ir ** 2))
        M = 1 << int(np.ceil(np.log2(N + L)))
        wet[ch] = np.fft.irfft(np.fft.rfft(out[ch], M) * np.fft.rfft(ir, M), M)[:N]
    mix = out + 0.32 * wet

    # level: quiet background, fades at both ends
    mix /= np.max(np.abs(mix))
    rms = np.sqrt(np.mean(mix ** 2))
    mix *= 10 ** (level_db / 20) / rms
    mix = np.clip(mix, -0.89, 0.89)
    fade = np.ones(N)
    fi, fo = int(2.5 * SR), int(3.5 * SR)
    fade[:fi] = np.linspace(0, 1, fi) ** 2
    fade[-fo:] = np.linspace(1, 0, fo) ** 1.5
    mix *= fade
    pcm = (mix.T * 32767).astype(np.int16)
    with wave.open(OUT, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print('wrote', OUT, 'peak dBFS', round(20 * np.log10(np.max(np.abs(mix))), 1), 'rms dBFS', round(20 * np.log10(np.sqrt(np.mean(mix ** 2))), 1))


if __name__ == '__main__':
    drone(float(sys.argv[1]) if len(sys.argv) > 1 else 75.0, sys.argv[2] if len(sys.argv) > 2 else 'drone.wav')
