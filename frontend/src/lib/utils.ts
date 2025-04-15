import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const isNotCourse = (value: string | string[]): boolean => {
  if (Array.isArray(value)) return true;
  if (value === "  ") return true;
  return /^[A-Z]+\d+$/.test(value.trim());
};


