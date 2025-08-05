import React, { useState } from 'react';
import { QueryClient, QueryClientProvider, useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, List as ListIcon, CheckCircle, Circle, Trash2, Edit2, Save, X } from 'lucide-react';
import { listApi, taskApi } from './api';
import type { List, Task, CreateListRequest, CreateTaskRequest } from './api';

const queryClient = new QueryClient();

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <div className="min-h-screen bg-gradient-to-br from-blue-100 to-green-50 py-6">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <header className="mb-8 text-center">
                        <h1 className="text-5xl font-extrabold text-gray-900 mb-4">Task Manager</h1>
                        <p className="text-lg text-gray-600">Organize your tasks and lists efficiently</p>
                    </header>
                    <TodoApp />
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
                                    className={`p-4 rounded-xl border shadow-md transition-all duration-300 cursor-pointer
                                        ${selectedListId === list.id
                                            ? 'border-blue-500 bg-blue-50 transform scale-105'
                                            : 'border-gray-200 bg-white hover:bg-gray-50 hover:shadow-lg'
                                        }`}
                                    onClick={() => setSelectedListId(list.id)}
                                >
                                    <h3 className="text-lg font-semibold text-gray-900">{list.name}</h3>
                                    <p className="text-sm text-gray-600">{list.description}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* Tasks Panel */}
            <div className="lg:col-span-2">
                {selectedList ? (
                    <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-6">
                        <div className="flex items-center justify-between mb-6">
                            <div>
                                <h2 className="text-3xl font-bold text-gray-900">{selectedList.name}</h2>
                                <p className="text-gray-600 mt-1">{selectedList.description}</p>
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
                                {[...Array(4)].map((_, i) => (
                                    <div key={i} className="h-12 bg-gray-200 rounded animate-pulse" />
                                ))}
                            </div>
                        ) : (
                            <div className="space-y-3">
                                {tasks.length === 0 ? (
                                    <div className="text-center py-8 text-gray-500">
                                        <p>No tasks in this list yet.</p>
                                        <p>Add a task to get started!</p>
                                    </div>
                                ) : (
                                    tasks.map((task) => (
                                        <div
                                            key={task.id}
                                            className={`p-4 rounded-xl border shadow-md transition-all duration-300
                                                ${task.completed
                                                    ? 'border-green-500 bg-green-50'
                                                    : 'border-gray-200 bg-white hover:bg-gray-50 hover:shadow-lg'
                                                }`}
                                        >
                                            <h4 className={`text-lg font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                                                {task.title}
                                            </h4>
                                            <p className={`text-sm ${task.completed ? 'line-through text-gray-400' : 'text-gray-600'}`}>
                                                {task.description}
                                            </p>
                                        </div>
                                    ))
                                )}
                            </div>
                        )}
                    </div>
                ) : (
                    <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-12 text-center">
                        <ListIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                        <h3 className="text-lg font-medium text-gray-900 mb-2">Select a List</h3>
                        <p className="text-gray-600">Choose a list from the sidebar to view and manage its tasks.</p>
                    </div>
                )}
            </div>
        </div>
    );
}

function CreateListForm({ onSubmit, onCancel, isLoading }: { onSubmit: (data: CreateListRequest) => void; onCancel: () => void; isLoading: boolean }) {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (name.trim()) {
            onSubmit({ name: name.trim(), description: description.trim() });
            setName('');
            setDescription('');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="mb-4 p-4 border border-gray-200 rounded-lg bg-gray-50">
            <div className="space-y-3">
                <input
                    type="text"
                    placeholder="List name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    disabled={isLoading}
                    autoFocus
                />
                <textarea
                    placeholder="Description (optional)"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={2}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    disabled={isLoading}
                />
                <div className="flex space-x-2">
                    <button
                        type="submit"
                        disabled={!name.trim() || isLoading}
                        className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <Save className="h-4 w-4 mr-1" />
                        {isLoading ? 'Creating...' : 'Create'}
                    </button>
                    <button
                        type="button"
                        onClick={onCancel}
                        disabled={isLoading}
                        className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                        <X className="h-4 w-4 mr-1" />
                        Cancel
                    </button>
                </div>
            </div>
        </form>
    );
}

export default App;