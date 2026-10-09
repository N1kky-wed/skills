// mahoraga template: a film card that grows out of its place to fill the screen (motion layoutId FLIP) and plays
// with sound; Esc/X/backdrop shrinks it back. mp4 (with optional muted loop) or Vimeo. Needs: motion, lucide-react,
// next/image, Tailwind tokens bg-ink, bg-lime-300, bg-paper, text-moss, text-lime-50 (rename to your palette).
'use client'

import Image from 'next/image'
import { AnimatePresence, LayoutGroup, motion, useReducedMotion } from 'motion/react'
import { Play, X } from 'lucide-react'
import { useCallback, useEffect, useId, useRef, useState } from 'react'
import { createPortal } from 'react-dom'

const cn = (...parts: (string | false | null | undefined)[]) => parts.filter(Boolean).join(' ')

export type FilmSource =
	| { kind: 'mp4'; src: string; loop?: string }
	| { kind: 'vimeo'; id: string }

const EASE = [0.32, 0.72, 0, 1] as const

// One of careNext's films as a card in the page: a muted loop (or the poster) behind a play button. Pressing it grows
// the very same frame out of its place in the page to fill the screen, corners squaring as it goes, and the film
// starts with sound; closing shrinks it back into the page. Nothing pins: the section scrolls like any other.
export function Film({
	source,
	poster,
	title,
	meta,
	size = 'lg',
	className
}: {
	source: FilmSource
	poster: string
	title: string
	meta?: string
	// lg for a film that owns its section; sm for one of several in a grid
	size?: 'lg' | 'sm'
	className?: string
}) {
	const radius = size === 'lg' ? 40 : 28
	const [open, setOpen] = useState(false)
	const [mounted, setMounted] = useState(false)
	const reduced = useReducedMotion()
	const layoutId = useId()
	const trigger = useRef<HTMLButtonElement>(null)
	const close = useRef<HTMLButtonElement>(null)
	const video = useRef<HTMLVideoElement>(null)

	useEffect(() => setMounted(true), [])

	const shut = useCallback(() => {
		setOpen(false)
		requestAnimationFrame(() => trigger.current?.focus({ preventScroll: true }))
	}, [])

	// while the film is up: no page scroll behind it, Esc closes, focus sits on the close button
	useEffect(() => {
		if (!open) return
		const root = document.documentElement
		const before = root.style.overflow
		root.style.overflow = 'hidden'
		const onKey = (e: KeyboardEvent) => {
			if (e.key === 'Escape') shut()
		}
		window.addEventListener('keydown', onKey)
		close.current?.focus({ preventScroll: true })
		return () => {
			root.style.overflow = before
			window.removeEventListener('keydown', onKey)
		}
	}, [open, shut])

	const transition = reduced ? { duration: 0 } : { duration: 0.75, ease: EASE }

	const frame = (
		<>
			{source.kind === 'mp4' && source.loop ? (
				<video
					className="absolute inset-0 size-full object-cover"
					src={source.loop}
					poster={poster}
					autoPlay
					muted
					loop
					playsInline
					preload="metadata"
					aria-hidden
				/>
			) : (
				<Image
					src={poster}
					alt=""
					fill
					sizes={size === 'lg' ? '(min-width: 1400px) 1320px, 100vw' : '(min-width: 1024px) 640px, 100vw'}
					className="object-cover transition-transform duration-[1.2s] ease-(--ease-out-expo) group-hover/film:scale-[1.04]"
				/>
			)}
		</>
	)

	return (
		<LayoutGroup>
			<div className={cn('relative w-full', !className?.includes('aspect-') && 'aspect-video', className)}>
				{!open ? (
					<motion.div layoutId={layoutId} transition={transition} style={{ borderRadius: radius }} className="group/film absolute inset-0 overflow-hidden bg-ink">
						{frame}
						{size === 'lg' ? (
							<>
								<span aria-hidden className="absolute inset-0 bg-[linear-gradient(180deg,transparent_45%,rgb(20_27_15/0.75))]" />
								<button
									ref={trigger}
									type="button"
									onClick={() => setOpen(true)}
									aria-label={`Play ${title}`}
									className="group absolute inset-0 flex flex-col items-start justify-end p-5 text-left text-lime-50 sm:p-10"
								>
									<span className="absolute top-[38%] left-1/2 grid size-14 -translate-1/2 place-items-center rounded-full bg-lime-300 text-ink shadow-[0_20px_50px_-12px_rgb(20_27_15/0.7)] transition-transform duration-500 ease-(--ease-out-expo) group-hover:scale-110 group-active:scale-95 sm:top-1/2 sm:size-20 lg:size-24">
										<Play className="size-5 translate-x-0.5 sm:size-7" fill="currentColor" />
									</span>
									<span className="text-[clamp(1.15rem,2.6vw,2.25rem)] leading-tight font-medium tracking-[-0.02em]">{title}</span>
									{meta ? <span className="mt-1 text-[14px] text-lime-100/75">{meta}</span> : null}
								</button>
							</>
						) : (
							// a solid caption strip, so the title reads over any poster, light or dark
							<button
								ref={trigger}
								type="button"
								onClick={() => setOpen(true)}
								aria-label={`Play ${title}`}
								className="group absolute inset-0 flex items-end p-2.5 text-left"
							>
								<span className="flex w-full items-center gap-3 rounded-[20px] bg-paper/95 py-2.5 pr-4 pl-2.5 shadow-[0_12px_30px_-18px_rgb(20_27_15/0.7)] transition-transform duration-500 ease-(--ease-out-expo) group-hover:-translate-y-1">
									<span className="grid size-11 shrink-0 place-items-center rounded-full bg-lime-300 text-ink transition-transform duration-500 ease-(--ease-out-expo) group-hover:scale-110 group-active:scale-95">
										<Play size={17} fill="currentColor" className="translate-x-px" />
									</span>
									<span className="min-w-0">
										<span className="block truncate text-[15px] leading-tight font-semibold tracking-[-0.01em] text-ink">{title}</span>
										{meta ? <span className="block truncate text-[12px] text-moss">{meta}</span> : null}
									</span>
								</span>
							</button>
						)}
					</motion.div>
				) : null}
			</div>

			{mounted
				? createPortal(
						<AnimatePresence>
							{open ? (
								<div role="dialog" aria-modal="true" aria-label={title} className="fixed inset-0 z-[100] grid place-items-center">
									<motion.button
										type="button"
										aria-label="Close film"
										tabIndex={-1}
										onClick={shut}
										className="absolute inset-0 bg-[#0b0f08]/92"
										initial={{ opacity: 0 }}
										animate={{ opacity: 1 }}
										exit={{ opacity: 0 }}
										transition={transition}
									/>
									<motion.div
										layoutId={layoutId}
										transition={transition}
										style={{ borderRadius: 0 }}
										className="relative aspect-video w-[min(100vw,calc(100svh*16/9))] overflow-hidden bg-black"
									>
										{source.kind === 'mp4' ? (
											<video
												ref={video}
												className="absolute inset-0 size-full object-contain"
												src={source.src}
												poster={poster}
												autoPlay
												controls
												playsInline
											/>
										) : (
											<iframe
												className="absolute inset-0 size-full"
												src={`https://player.vimeo.com/video/${source.id}?autoplay=1&dnt=1&title=0&byline=0&portrait=0`}
												title={title}
												allow="autoplay; fullscreen; picture-in-picture"
												allowFullScreen
											/>
										)}
									</motion.div>
									<motion.button
										ref={close}
										type="button"
										onClick={shut}
										aria-label="Close film"
										initial={{ opacity: 0, scale: 0.8 }}
										animate={{ opacity: 1, scale: 1, transition: { delay: reduced ? 0 : 0.35, duration: 0.4 } }}
										exit={{ opacity: 0, scale: 0.8, transition: { duration: 0.15 } }}
										className="absolute top-5 right-5 grid size-12 place-items-center rounded-full bg-lime-300 text-ink shadow-[0_12px_30px_-10px_rgb(0_0_0/0.6)] transition-transform hover:scale-105 active:scale-95"
									>
										<X size={20} />
									</motion.button>
								</div>
							) : null}
						</AnimatePresence>,
						document.body
					)
				: null}
		</LayoutGroup>
	)
}
