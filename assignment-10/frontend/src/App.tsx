import React, { useState, useEffect } from 'react';
import { QueryClient, QueryClientProvider, useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, List as ListIcon, CheckCircle, Circle, Trash2, Edit2, Save, X } from 'lucide-react';
import { listApi, taskApi, authApi } from './api';
import type { List, Task, CreateListRequest, CreateTaskRequest } from './api';
import { AuthContainer } from './components/AuthContainer';
import { Header } from './components/Header';

const queryClient = new QueryClient();

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            setIsAuthenticated(true);
        }
    }, []);

    const handleAuthSuccess = () => {
        setIsAuthenticated(true);
    };

    const handleLogout = () => {
        authApi.logout();
        setIsAuthenticated(false);
    };

    if (!isAuthenticated) {
        return (
            <QueryClientProvider client={queryClient}>
                <AuthContainer onAuthSuccess={handleAuthSuccess} />
            </QueryClientProvider>
        );
    }

    return (
        <QueryClientProvider client={queryClient}>
            <div className="min-h-screen bg-gradient-to-br from-blue-100 to-green-50">
                <Header onLogout={handleLogout} />
                <div className="py-6">
                    <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                        <TodoApp />
                    </div>
                </div>
            </div>
        </QueryClientProvider>
    );
}

function TodoApp() {
    const [selectedListId, setSelectedListId] = useState<string | null>(null);
    const [isCreatingList, setIsCreatingList] = useState(false);
    const [isCreatingTask, setIsCreatingTask] = useState(false);
    const [editingList, setEditingList] = useState<string | null>(null);
    const [editingTask, setEditingTask] = useState<string | null>(null);

    const queryClient = useQueryClient();

    const { data: lists = [], isLoading: listsLoading } = useQuery({
        queryKey: ['lists'],
        queryFn: listApi.getLists,
    });

    const { data: tasks = [], isLoading: tasksLoading } = useQuery({
        queryKey: ['tasks', selectedListId],
        queryFn: () => (selectedListId ? taskApi.getTasksByList(selectedListId) : Promise.resolve([])),
        enabled: !!selectedListId,
    });

    const createListMutation = useMutation({
        mutationFn: listApi.createList,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['lists'] });
            setIsCreatingList(false);
        },
    });

    const createTaskMutation = useMutation({
        mutationFn: taskApi.createTask,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['tasks', selectedListId] });
            setIsCreatingTask(false);
        },
    });

    const selectedList = lists.find((list) => list.id === selectedListId);

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Lists Panel */}
            <div className="lg:col-span-1">
                <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                            <ListIcon className="mr-2 h-6 w-6 text-blue-600" />
                            Lists
                        </h2>
                        <button
                            onClick={() => setIsCreatingList(true)}
                            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-300"
                        >
                            <Plus className="h-5 w-5 mr-1" />
                            Add List
                        </button>
                    </div>

                    {isCreatingList && (
                        <CreateListForm
                            onSubmit={(data) => createListMutation.mutate(data)}
                            onCancel={() => setIsCreatingList(false)}
                            isLoading={createListMutation.isPending}
                        />
                    )}

                    {listsLoading ? (
                        <div className="space-y-2">
                            {[...Array(3)].map((_, i) => (
                                <div key={i} className="h-16 bg-gray-200 rounded animate-pulse" />
                            ))}
                        </div>
                    ) : (
                        <div className="space-y-2">
                            {lists.map((list) => (
                                <div
                                    key={list.id}
                                    className={`p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
                                        selectedListId === list.id
                                            ? 'border-blue-500 bg-blue-50'
                                            : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                                    }`}
                                    onClick={() => setSelectedListId(list.id)}
                                >
                                    <div className="flex items-center justify-between">
                                        <div className="flex-1">
                                            <h3 className="font-semibold text-gray-900">{list.name}</h3>
                                            {list.description && (
                                                <p className="text-sm text-gray-600 mt-1">{list.description}</p>
                                            )}
                                        </div>
                                        <div className="flex items-center space-x-2">
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    setEditingList(list.id);
                                                }}
                                                className="p-1 text-gray-400 hover:text-blue-600 transition-colors"
                                            >
                                                <Edit2 className="h-4 w-4" />
                                            </button>
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    // Handle delete
                                                }}
                                                className="p-1 text-gray-400 hover:text-red-600 transition-colors"
                                            >
                                                <Trash2 className="h-4 w-4" />
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* Tasks Panel */}
            <div className="lg:col-span-2">
                <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-6">
                    {selectedList ? (
                        <div>
                            <div className="flex items-center justify-between mb-6">
                                <div>
                                    <h2 className="text-2xl font-bold text-gray-900">{selectedList.name}</h2>
                                    {selectedList.description && (
                                        <p className="text-gray-600 mt-1">{selectedList.description}</p>
                                    )}
                                </div>
                                <button
                                    onClick={() => setIsCreatingTask(true)}
                                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors duration-300"
                                >
                                    <Plus className="h-5 w-5 mr-1" />
                                    Add Task
                                </button>
                            </div>

                            {isCreatingTask && (
                                <CreateTaskForm
                                    listId={selectedListId!}
                                    onSubmit={(data) => createTaskMutation.mutate(data)}
                                    onCancel={() => setIsCreatingTask(false)}
                                    isLoading={createTaskMutation.isPending}
                                />
                            )}

                            {tasksLoading ? (
                                <div className="space-y-3">
                                    {[...Array(3)].map((_, i) => (
                                        <div key={i} className="h-16 bg-gray-200 rounded animate-pulse" />
                                    ))}
                                </div>
                            ) : (
                                <div className="space-y-3">
                                    {tasks.map((task) => (
                                        <TaskItem key={task.id} task={task} />
                                    ))}
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="text-center py-12">
                            <div className="text-gray-400 mb-4">
                                <ListIcon className="h-16 w-16 mx-auto" />
                            </div>
                            <h3 className="text-lg font-medium text-gray-900 mb-2">No list selected</h3>
                            <p className="text-gray-600">Select a list from the sidebar to view its tasks</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

function CreateListForm({ onSubmit, onCancel, isLoading }: { onSubmit: (data: CreateListRequest) => void; onCancel: () => void; isLoading: boolean }) {
    const [formData, setFormData] = useState<CreateListRequest>({ name: '', description: '' });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4 p-4 bg-gray-50 rounded-lg mb-4">
            <div>
                <input
                    type="text"
                    placeholder="List name"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                />
            </div>
            <div>
                <textarea
                    placeholder="Description (optional)"
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={2}
                />
            </div>
            <div className="flex space-x-2">
                <button
                    type="submit"
                    disabled={isLoading}
                    className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                >
                    {isLoading ? 'Creating...' : 'Create List'}
                </button>
                <button
                    type="button"
                    onClick={onCancel}
                    className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
                >
                    Cancel
                </button>
            </div>
        </form>
    );
}

function CreateTaskForm({ listId, onSubmit, onCancel, isLoading }: { listId: string; onSubmit: (data: CreateTaskRequest) => void; onCancel: () => void; isLoading: boolean }) {
    const [formData, setFormData] = useState<CreateTaskRequest>({ title: '', description: '', list_id: listId });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4 p-4 bg-gray-50 rounded-lg mb-4">
            <div>
                <input
                    type="text"
                    placeholder="Task title"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                />
            </div>
            <div>
                <textarea
                    placeholder="Description (optional)"
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={2}
                />
            </div>
            <div className="flex space-x-2">
                <button
                    type="submit"
                    disabled={isLoading}
                    className="flex-1 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
                >
                    {isLoading ? 'Creating...' : 'Create Task'}
                </button>
                <button
                    type="button"
                    onClick={onCancel}
                    className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
                >
                    Cancel
                </button>
            </div>
        </form>
    );
}

function TaskItem({ task }: { task: Task }) {
    const [isEditing, setIsEditing] = useState(false);
    const [editData, setEditData] = useState({ title: task.title, description: task.description });

    const queryClient = useQueryClient();

    const updateTaskMutation = useMutation({
        mutationFn: (data: Partial<CreateTaskRequest & { completed: boolean }>) =>
            taskApi.updateTask(task.id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['tasks'] });
            setIsEditing(false);
        },
    });

    const toggleTaskMutation = useMutation({
        mutationFn: () => taskApi.toggleTask(task.id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['tasks'] });
        },
    });

    const deleteTaskMutation = useMutation({
        mutationFn: () => taskApi.deleteTask(task.id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['tasks'] });
        },
    });

    const handleSave = () => {
        updateTaskMutation.mutate(editData);
    };

    const handleCancel = () => {
        setEditData({ title: task.title, description: task.description });
        setIsEditing(false);
    };

    if (isEditing) {
        return (
            <div className="p-4 border border-gray-200 rounded-lg bg-white">
                <div className="space-y-3">
                    <input
                        type="text"
                        value={editData.title}
                        onChange={(e) => setEditData({ ...editData, title: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <textarea
                        value={editData.description}
                        onChange={(e) => setEditData({ ...editData, description: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        rows={2}
                    />
                    <div className="flex space-x-2">
                        <button
                            onClick={handleSave}
                            disabled={updateTaskMutation.isPending}
                            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                        >
                            <Save className="h-4 w-4" />
                        </button>
                        <button
                            onClick={handleCancel}
                            className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
                        >
                            <X className="h-4 w-4" />
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="p-4 border border-gray-200 rounded-lg bg-white hover:shadow-md transition-shadow">
            <div className="flex items-start space-x-3">
                <button
                    onClick={() => toggleTaskMutation.mutate()}
                    className="mt-1 text-gray-400 hover:text-green-600 transition-colors"
                >
                    {task.completed ? <CheckCircle className="h-5 w-5 text-green-600" /> : <Circle className="h-5 w-5" />}
                </button>
                <div className="flex-1">
                    <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                        {task.title}
                    </h3>
                    {task.description && (
                        <p className={`text-sm mt-1 ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                            {task.description}
                        </p>
                    )}
                </div>
                <div className="flex items-center space-x-1">
                    <button
                        onClick={() => setIsEditing(true)}
                        className="p-1 text-gray-400 hover:text-blue-600 transition-colors"
                    >
                        <Edit2 className="h-4 w-4" />
                    </button>
                    <button
                        onClick={() => deleteTaskMutation.mutate()}
                        className="p-1 text-gray-400 hover:text-red-600 transition-colors"
                    >
                        <Trash2 className="h-4 w-4" />
                    </button>
                </div>
            </div>
        </div>
    );
}

export default App;