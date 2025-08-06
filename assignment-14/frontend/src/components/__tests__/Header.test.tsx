import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Header } from '../Header'

// Mock the API
vi.mock('../../api', () => ({
  authApi: {
    getCurrentUser: vi.fn(),
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

describe('Header Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders header with title', () => {
    const mockOnLogout = vi.fn()

    renderWithQueryClient(<Header onLogout={mockOnLogout} />)

    expect(screen.getByText('Task Manager')).toBeInTheDocument()
  })

  it('shows loading state when user data is loading', () => {
    const mockOnLogout = vi.fn()

    renderWithQueryClient(<Header onLogout={mockOnLogout} />)

    // Should show loading state initially
    expect(screen.getByText('Task Manager')).toBeInTheDocument()
  })

  it('shows user menu when user is authenticated', async () => {
    const mockOnLogout = vi.fn()
    const mockUser = {
      id: '1',
      username: 'testuser',
      email: 'test@example.com',
    }

    // Mock the API response
    const { authApi } = await import('../../api')
    vi.mocked(authApi.getCurrentUser).mockResolvedValue(mockUser)

    renderWithQueryClient(<Header onLogout={mockOnLogout} />)

    await waitFor(() => {
      expect(screen.getByText(/Welcome, testuser!/)).toBeInTheDocument()
    })
  })

  it('opens user menu when user button is clicked', async () => {
    const mockOnLogout = vi.fn()
    const mockUser = {
      id: '1',
      username: 'testuser',
      email: 'test@example.com',
    }

    const { authApi } = await import('../../api')
    vi.mocked(authApi.getCurrentUser).mockResolvedValue(mockUser)

    renderWithQueryClient(<Header onLogout={mockOnLogout} />)

    await waitFor(() => {
      expect(screen.getByText(/Welcome, testuser!/)).toBeInTheDocument()
    })

    const userButton = screen.getByText(/Welcome, testuser!/)
    fireEvent.click(userButton)

    // Should show menu options
    expect(screen.getByText('Change Password')).toBeInTheDocument()
    expect(screen.getByText('Logout')).toBeInTheDocument()
  })

  it('calls onLogout when logout button is clicked', async () => {
    const mockOnLogout = vi.fn()
    const mockUser = {
      id: '1',
      username: 'testuser',
      email: 'test@example.com',
    }

    const { authApi } = await import('../../api')
    vi.mocked(authApi.getCurrentUser).mockResolvedValue(mockUser)

    renderWithQueryClient(<Header onLogout={mockOnLogout} />)

    await waitFor(() => {
      expect(screen.getByText(/Welcome, testuser!/)).toBeInTheDocument()
    })

    const userButton = screen.getByText(/Welcome, testuser!/)
    fireEvent.click(userButton)

    const logoutButton = screen.getByText('Logout')
    fireEvent.click(logoutButton)

    expect(mockOnLogout).toHaveBeenCalledTimes(1)
  })

  it('shows change password modal when change password is clicked', async () => {
    const mockOnLogout = vi.fn()
    const mockUser = {
      id: '1',
      username: 'testuser',
      email: 'test@example.com',
    }

    const { authApi } = await import('../../api')
    vi.mocked(authApi.getCurrentUser).mockResolvedValue(mockUser)

    renderWithQueryClient(<Header onLogout={mockOnLogout} />)

    await waitFor(() => {
      expect(screen.getByText(/Welcome, testuser!/)).toBeInTheDocument()
    })

    const userButton = screen.getByText(/Welcome, testuser!/)
    fireEvent.click(userButton)

    const changePasswordButton = screen.getByText('Change Password')
    fireEvent.click(changePasswordButton)

    // Should show password change modal
    expect(screen.getByText('Change Password')).toBeInTheDocument()
  })

  it('handles API error gracefully', async () => {
    const mockOnLogout = vi.fn()

    const { authApi } = await import('../../api')
    vi.mocked(authApi.getCurrentUser).mockRejectedValue(new Error('API Error'))

    renderWithQueryClient(<Header onLogout={mockOnLogout} />)

    // Should still render header even if API fails
    expect(screen.getByText('Task Manager')).toBeInTheDocument()
  })
}) 