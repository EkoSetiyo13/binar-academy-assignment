import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Login } from '../Login'

// Mock the API
vi.mock('../../api', () => ({
  authApi: {
    login: vi.fn(),
  },
}))

const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
      mutations: {
        retry: false,
      },
    },
  })

const renderWithQueryClient = (component: React.ReactElement) => {
  const queryClient = createTestQueryClient()
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  )
}

describe('Login Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders login form', () => {
    const mockOnSwitchToRegister = vi.fn()
    const mockOnLoginSuccess = vi.fn()

    renderWithQueryClient(
      <Login onSwitchToRegister={mockOnSwitchToRegister} onLoginSuccess={mockOnLoginSuccess} />
    )

    expect(screen.getByText('Login')).toBeInTheDocument()
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /register/i })).toBeInTheDocument()
  })

  it('handles form input changes', () => {
    const mockOnSwitchToRegister = vi.fn()
    const mockOnLoginSuccess = vi.fn()

    renderWithQueryClient(
      <Login onSwitchToRegister={mockOnSwitchToRegister} onLoginSuccess={mockOnLoginSuccess} />
    )

    const usernameInput = screen.getByLabelText(/username/i)
    const passwordInput = screen.getByLabelText(/password/i)

    fireEvent.change(usernameInput, { target: { value: 'testuser' } })
    fireEvent.change(passwordInput, { target: { value: 'password123' } })

    expect(usernameInput).toHaveValue('testuser')
    expect(passwordInput).toHaveValue('password123')
  })

  it('toggles password visibility', () => {
    const mockOnSwitchToRegister = vi.fn()
    const mockOnLoginSuccess = vi.fn()

    renderWithQueryClient(
      <Login onSwitchToRegister={mockOnSwitchToRegister} onLoginSuccess={mockOnLoginSuccess} />
    )

    const passwordInput = screen.getByLabelText(/password/i)
    const toggleButton = screen.getByRole('button', { name: /toggle password visibility/i })

    expect(passwordInput).toHaveAttribute('type', 'password')

    fireEvent.click(toggleButton)
    expect(passwordInput).toHaveAttribute('type', 'text')

    fireEvent.click(toggleButton)
    expect(passwordInput).toHaveAttribute('type', 'password')
  })

  it('calls onSwitchToRegister when register button is clicked', () => {
    const mockOnSwitchToRegister = vi.fn()
    const mockOnLoginSuccess = vi.fn()

    renderWithQueryClient(
      <Login onSwitchToRegister={mockOnSwitchToRegister} onLoginSuccess={mockOnLoginSuccess} />
    )

    const registerButton = screen.getByRole('button', { name: /register/i })
    fireEvent.click(registerButton)

    expect(mockOnSwitchToRegister).toHaveBeenCalledTimes(1)
  })

  it('shows validation error for empty fields', async () => {
    const mockOnSwitchToRegister = vi.fn()
    const mockOnLoginSuccess = vi.fn()

    renderWithQueryClient(
      <Login onSwitchToRegister={mockOnSwitchToRegister} onLoginSuccess={mockOnLoginSuccess} />
    )

    const loginButton = screen.getByRole('button', { name: /login/i })
    fireEvent.click(loginButton)

    await waitFor(() => {
      expect(screen.getByText(/username is required/i)).toBeInTheDocument()
      expect(screen.getByText(/password is required/i)).toBeInTheDocument()
    })
  })

  it('handles successful login', async () => {
    const mockOnSwitchToRegister = vi.fn()
    const mockOnLoginSuccess = vi.fn()
    const mockLoginResponse = {
      access_token: 'test-token',
      token_type: 'bearer',
    }

    // Mock localStorage
    const localStorageMock = {
      getItem: vi.fn(),
      setItem: vi.fn(),
      removeItem: vi.fn(),
      clear: vi.fn(),
    }
    Object.defineProperty(window, 'localStorage', {
      value: localStorageMock,
      writable: true,
    })

    renderWithQueryClient(
      <Login onSwitchToRegister={mockOnSwitchToRegister} onLoginSuccess={mockOnLoginSuccess} />
    )

    const usernameInput = screen.getByLabelText(/username/i)
    const passwordInput = screen.getByLabelText(/password/i)
    const loginButton = screen.getByRole('button', { name: /login/i })

    fireEvent.change(usernameInput, { target: { value: 'testuser' } })
    fireEvent.change(passwordInput, { target: { value: 'password123' } })
    fireEvent.click(loginButton)

    await waitFor(() => {
      expect(localStorageMock.setItem).toHaveBeenCalledWith('access_token', 'test-token')
      expect(mockOnLoginSuccess).toHaveBeenCalledTimes(1)
    })
  })

  it('shows error message on login failure', async () => {
    const mockOnSwitchToRegister = vi.fn()
    const mockOnLoginSuccess = vi.fn()

    renderWithQueryClient(
      <Login onSwitchToRegister={mockOnSwitchToRegister} onLoginSuccess={mockOnLoginSuccess} />
    )

    const usernameInput = screen.getByLabelText(/username/i)
    const passwordInput = screen.getByLabelText(/password/i)
    const loginButton = screen.getByRole('button', { name: /login/i })

    fireEvent.change(usernameInput, { target: { value: 'testuser' } })
    fireEvent.change(passwordInput, { target: { value: 'wrongpassword' } })
    fireEvent.click(loginButton)

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument()
    })
  })
}) 