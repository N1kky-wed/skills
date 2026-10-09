'use client'

import { animate, useInView, useReducedMotion } from 'motion/react'
import { useEffect, useRef, useState } from 'react'

// Counts up to a figure the first time it scrolls into view. The final text renders on the server, so the number is
// there without script; the count replaces it only while it runs.
export function CountUp({ to, decimals = 0, suffix = '', className }: { to: number; decimals?: number; suffix?: string; className?: string }) {
	const ref = useRef<HTMLSpanElement>(null)
	const inView = useInView(ref, { once: true, margin: '0px 0px -15% 0px' })
	const reduced = useReducedMotion()
	const [value, setValue] = useState<number | null>(null)

	useEffect(() => {
		if (!inView || reduced) return
		const controls = animate(0, to, { duration: 1.6, ease: [0.16, 1, 0.3, 1], onUpdate: setValue, onComplete: () => setValue(null) })
		return () => controls.stop()
	}, [inView, reduced, to])

	const shown = value == null ? to : value
	return (
		<span ref={ref} className={className}>
			{shown.toFixed(decimals)}
			{suffix}
		</span>
	)
}
