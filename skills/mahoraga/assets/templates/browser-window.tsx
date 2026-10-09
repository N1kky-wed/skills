// mahoraga template: show web products in a browser window (and tablet apps on a tablet), never a phone.
const cn = (...parts: (string | false | null | undefined)[]) => parts.filter(Boolean).join(' ')

// careNext's tools are websites (Doc360°, the careSumerPAY application, careNextVault) and one tablet app
// (careNextER), so the products are shown in a browser window and a tablet, never a phone.

export function BrowserWindow({ url, children, className }: { url: React.ReactNode; children: React.ReactNode; className?: string }) {
	return (
		<div className={cn('overflow-hidden rounded-[22px] bg-paper shadow-[0_50px_90px_-40px_rgb(20_27_15/0.7),0_0_0_1px_rgb(20_27_15/0.08)]', className)}>
			<div className="flex items-center gap-2 border-b border-ink/8 bg-cream-2 px-4 py-3">
				<span className="size-2.5 rounded-full bg-[#ff5f57]" />
				<span className="size-2.5 rounded-full bg-[#febc2e]" />
				<span className="size-2.5 rounded-full bg-[#28c840]" />
				<span className="mx-auto flex h-6 w-[min(22rem,60%)] items-center justify-center truncate rounded-md bg-white px-3 text-[11px] text-moss ring-1 ring-ink/[0.06]">
					{url}
				</span>
				<span className="w-[46px]" />
			</div>
			{children}
		</div>
	)
}

export function Tablet({ children, className }: { children: React.ReactNode; className?: string }) {
	return (
		<div className={cn('rounded-[34px] bg-[#0d0f0b] p-3 shadow-[0_50px_90px_-40px_rgb(20_27_15/0.75)]', className)}>
			<div className="overflow-hidden rounded-[24px] bg-[#f8f6f1]">{children}</div>
		</div>
	)
}
