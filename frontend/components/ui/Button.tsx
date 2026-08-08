import React from "react";
import { cn } from "@/lib/utils/cn";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost";
  size?: "sm" | "md" | "lg";
}

export function Button({
  className,
  variant = "primary",
  size = "md",
  children,
  ...props
}: ButtonProps) {
  const baseStyle =
    "inline-flex items-center justify-center font-medium rounded-lg transition-all focus:outline-none focus:ring-2 focus:ring-sky-500/50 disabled:opacity-50 disabled:cursor-not-allowed";

  const variants = {
    primary: "bg-sky-600 hover:bg-sky-500 text-white shadow-lg shadow-sky-900/30 border border-sky-400/30",
    secondary: "bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700",
    outline: "border border-sky-500/40 text-sky-300 hover:bg-sky-500/10",
    ghost: "text-slate-400 hover:text-slate-100 hover:bg-slate-800/60",
  };

  const sizes = {
    sm: "px-3 py-1.5 text-xs",
    md: "px-4 py-2 text-sm",
    lg: "px-6 py-3 text-base",
  };

  return (
    <button className={cn(baseStyle, variants[variant], sizes[size], className)} {...props}>
      {children}
    </button>
  );
}
