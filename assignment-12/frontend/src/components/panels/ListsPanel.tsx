import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, List as ListIcon } from 'lucide-react';
import { listApi } from '../../api';
import { CreateListForm } from '../forms';
import { ListItem } from '../lists/ListItem';
import type { List, CreateListRequest } from '../../types';

interface ListsPanelProps {
  selectedListId: string | null;
  onListSelect: (id: string) => void;
}

export function ListsPanel({ selectedListId, onListSelect }: ListsPanelProps) {
  const [isCreatingList, setIsCreatingList] = useState(false);
  const [editingList, setEditingList] = useState<string | null>(null);

  const queryClient = useQueryClient();

  const { data: lists = [], isLoading: listsLoading } = useQuery({
    queryKey: ['lists'],
    queryFn: listApi.getLists,
  });

  const createListMutation = useMutation({
    mutationFn: listApi.createList,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['lists'] });
      setIsCreatingList(false);
    },
  });

  const handleListEdit = (id: string) => {
    setEditingList(id);
    // TODO: Implement edit functionality
  };

  const handleListDelete = (id: string) => {
    // TODO: Implement delete functionality
    console.log('Delete list:', id);
  };

  return (
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
            <ListItem
              key={list.id}
              list={list}
              isSelected={selectedListId === list.id}
              onSelect={onListSelect}
              onEdit={handleListEdit}
              onDelete={handleListDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
} 