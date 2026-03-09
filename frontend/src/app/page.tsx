/**
 * Home page - redirects to signin for authentication
 */

import { redirect } from 'next/navigation'

export default function HomePage() {
  // Redirect to signin page for authentication
  redirect('/signin')
}
