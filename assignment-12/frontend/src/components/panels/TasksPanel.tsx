import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, List as ListIcon } from 'lucide-react';
import { taskApi, listApi } from '../../api';
import { CreateTaskForm } from '../forms';
import { TaskItem } from '../tasks/TaskItem';
import type { Task, CreateTaskRequest, List } from '../../types';

interface TasksPanelProps {
  selectedListId: string | null;
}

export function TasksPanel({ selectedListId }: TasksPanelProps) {
  const [isCreatingTask, setIsCreatingTask] = useState(false);

  const queryClient = useQueryClient();

  const { data: selectedList } = useQuery({
    queryKey: ['lists', selectedListId],
    queryFn: () => (selectedListId ? listApi.getList(selectedListId) : null),
    enabled: !!selectedListId,
  });

  const { data: tasks = [], isLoading: tasksLoading } = useQuery({
    queryKey: ['tasks', selectedListId],
    queryFn: () => (selectedListId ? taskApi.getTasksByList(selectedListId) : Promise.resolve([])),
    enabled: !!selectedListId,
  });

  const createTaskMutation = useMutation({
    mutationFn: taskApi.createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks', selectedListId] });
      setIsCreatingTask(false);
    },
  });

  if (!selectedList) {
    return (
      <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-6">
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <ListIcon className="h-16 w-16 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No list selected</h3>
          <p className="text-gray-600">Select a list from the sidebar to view its tasks</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-6">
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
  );
} 