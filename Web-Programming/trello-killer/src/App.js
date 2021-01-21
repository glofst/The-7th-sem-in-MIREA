import React, {useState} from 'react';
import {DragDropContext, Droppable, Draggable} from 'react-beautiful-dnd';
import { v4 as uuid } from 'uuid';
import './App.css'
let tasks = [
  {
    id: 'Task 1',
    name: 'Task 1',
  },
  {
    id: 'Task 2',
    name: 'Task 2',
  },
  {
    id: 'Task 3',
    name: 'Task 3',
  },
  {
    id: 'Task 4',
    name: 'Task 4',
  },
  {
    id: 'Task 5',
    name: 'Task 5',
  },
  {
    id: 'Task 6',
    name: 'Task 6',
  }
]

const columnsAll =
  {
    [uuid()]: {
      name: 'To Do',
      items: tasks
    },
    [uuid()]: {
      name: 'In Process',
      items: []
    },
    [uuid()]: {
      name: 'Done',
      items: []
    }
  }

const onDragEnd = (result, columns, setColumns) => {
  if(!result.destination) return;
  const {source, destination} = result;
  if(source.droppableId !== destination.droppableId) {
    const sourceColumn = columns[source.droppableId];
    const destinationColumn = columns[destination.droppableId];
    const sourceItems = [...sourceColumn.items];
    const destinationItems = [...destinationColumn.items];
    const [removed] = sourceItems.splice(source.index, 1);
    destinationItems.splice(destination.index, 0, removed);
    setColumns({
      ...columns,
      [source.droppableId]: {
        ...sourceColumn,
        items:sourceItems
      },
      [destination.droppableId]: {
        ...destinationColumn,
        items: destinationItems
      }
    })
  } else {
    const column = columns[source.droppableId];
    const copiedItems = [...column.items]
    const [removed] = copiedItems.splice(source.index, 1);
    copiedItems.splice(destination.index, 0, removed);
    setColumns({
      ...columns,
      [source.droppableId]: {
        ...column,
        items: copiedItems
      }
    })
  }

}

function App() {
  const [columns, setColumns] = useState(columnsAll);

  return (
    <div className="App" style={{display: 'flex', justifyContent: 'center', height: '100%'}}>
      <DragDropContext onDragEnd={result => onDragEnd(result, columns, setColumns)}>
        {Object.entries(columns).map(([id, column]) => {
          return(
            <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
              <div>
                <h2 class='colHead'>{column.name}</h2>
              </div>
              <script type='text/javascript'>
              </script>
              <div style={{margin: 5}}>
                <Droppable droppableId={id} key={id}>
                  {(provided, snapshot) => {
                    return(
                      <div class='column' {...provided.droppableProps} ref={provided.innerRef} style={{padding: 4, width: 250, minHeight:500 }}>
                        {column.items.map((item, index) => {
                          return(
                            <Draggable key={item.id} draggableId={item.id} index={index}>
                              {(provided, snapshot) => {
                                return(
                                  <div ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps} style={{userSelect: 'none', padding: 16, margin: '0 0 8px 0', minHeight: '50px', backgroundColor: snapshot.isDragging ? '#1f1a1a' : '#1f1a1a', color: 'white', ...provided.draggableProps.style}}>
                                    {item.name}
                                  </div>
                                )
                              }}
                            </Draggable>
                          )
                        })}
                        {provided.placeholder}
                      </div>
                    )
                  }}
                </Droppable>
              </div>
            </div>
          )
        })}
      </DragDropContext>
    </div>
  );
}


export default App;
