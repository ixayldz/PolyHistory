import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: string | Date): string {
  return new Date(date).toLocaleDateString('tr-TR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

export function getConfidenceColor(label: string): string {
  switch (label) {
    case 'high':
      return 'bg-green-500'
    case 'medium':
      return 'bg-yellow-500'
    case 'low':
      return 'bg-red-500'
    default:
      return 'bg-gray-500'
  }
}

export function getSourceTypeColor(type: string): string {
  switch (type) {
    case 'primary':
      return 'border-l-green-500'
    case 'academic':
      return 'border-l-blue-500'
    case 'secondary':
      return 'border-l-indigo-500'
    case 'memoir':
      return 'border-l-purple-500'
    case 'press':
      return 'border-l-yellow-500'
    default:
      return 'border-l-gray-500'
  }
}

export function getStanceColor(stance: string): string {
  switch (stance) {
    case 'support':
    case 'pro':
      return 'text-green-600 bg-green-50'
    case 'oppose':
    case 'contra':
      return 'text-red-600 bg-red-50'
    case 'neutral':
      return 'text-gray-600 bg-gray-50'
    default:
      return 'text-gray-600 bg-gray-50'
  }
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength) + '...'
}
