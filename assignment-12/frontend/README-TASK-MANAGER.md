# Task Manager Frontend

A modern, responsive task management application built with React, TypeScript, and Vite.

## Features

- ✅ Create and manage lists
- ✅ Add, edit, and delete tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Real-time updates with React Query
- ✅ Beautiful, responsive UI with Tailwind CSS
- ✅ TypeScript for type safety

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **React Query (@tanstack/react-query)** - Server state management
- **Axios** - HTTP client
- **Lucide React** - Icons

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running on `http://localhost:8000`

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## API Integration

The frontend integrates with a FastAPI backend with the following endpoints:

### Lists
- `GET /lists` - Get all lists
- `POST /lists` - Create a new list
- `GET /lists/{id}` - Get a specific list
- `PUT /lists/{id}` - Update a list
- `DELETE /lists/{id}` - Delete a list

### Tasks
- `GET /tasks` - Get all tasks
- `GET /lists/{list_id}/tasks` - Get tasks for a specific list
- `POST /tasks` - Create a new task
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task
- `PATCH /tasks/{id}/toggle` - Toggle task completion

## Environment Variables

- `VITE_API_BASE_URL` - Backend API base URL (default: http://localhost:8000)

## Features Overview

### Lists Management
- Create new lists with name and description
- Edit existing lists inline
- Delete lists with confirmation
- Visual selection indicator

### Tasks Management
- Add tasks to selected lists
- Mark tasks as complete/incomplete
- Edit task details inline
- Delete tasks with confirmation
- Visual completion status

### UI/UX Features
- Responsive design for all screen sizes
- Loading states and optimistic updates
- Error handling and user feedback
- Clean, modern interface
- Accessible design patterns
