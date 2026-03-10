const TOKEN_KEY = 'access_token'
const USER_KEY = 'current_user'
const AUTH_CHANGED_EVENT = 'auth-changed'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY) || ''
}

export function setToken(token) {
  if (!token) return
  localStorage.setItem(TOKEN_KEY, token)
  window.dispatchEvent(new CustomEvent(AUTH_CHANGED_EVENT))
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
  window.dispatchEvent(new CustomEvent(AUTH_CHANGED_EVENT))
}

export function setCurrentUser(user) {
  if (!user) {
    localStorage.removeItem(USER_KEY)
  } else {
    localStorage.setItem(USER_KEY, JSON.stringify(user))
  }
  window.dispatchEvent(new CustomEvent(AUTH_CHANGED_EVENT))
}

export function getCurrentUser() {
  try {
    const raw = localStorage.getItem(USER_KEY)
    return raw ? JSON.parse(raw) : null
  } catch (e) {
    return null
  }
}

export function isLoggedIn() {
  return Boolean(getToken())
}

export function getAuthChangedEventName() {
  return AUTH_CHANGED_EVENT
}
