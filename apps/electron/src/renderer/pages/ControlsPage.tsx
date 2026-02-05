import React from 'react';
import { useItakBridge } from '@hooks/cli-adapter';

export function ControlsPage() {
  const {
    processState,
    busyFlag,
    initiateAgent,
    terminateAgent,
    executeCommand,
    transmitInput,
  } = useItakBridge();
  
  const [commandText, setCommandText] = React.useState('');
  const [commandArgs, setCommandArgs] = React.useState('');
  const [inputText, setInputText] = React.useState('');
  
  const handleStartAgent = async () => {
    await initiateAgent();
  };
  
  const handleStopAgent = async () => {
    await terminateAgent();
  };
  
  const handleRunCommand = async () => {
    if (!commandText.trim()) return;
    
    const args = commandArgs.trim() 
      ? commandArgs.split(' ').filter(a => a.length > 0)
      : undefined;
    
    await executeCommand(commandText.trim(), args);
    setCommandText('');
    setCommandArgs('');
  };
  
  const handleSendInput = async () => {
    if (!inputText.trim()) return;
    
    await transmitInput(inputText.trim());
    setInputText('');
  };
  
  return (
    <div>
      <div className="card">
        <h2 className="card-header">Agent Controls</h2>
        
        <div className="flex gap-md">
          <button 
            className="btn btn-success"
            onClick={handleStartAgent}
            disabled={busyFlag || processState.active}
          >
            ▶️ Start Agent
          </button>
          
          <button 
            className="btn btn-danger"
            onClick={handleStopAgent}
            disabled={busyFlag || !processState.active}
          >
            ⏹️ Stop Agent
          </button>
        </div>
        
        <div style={{ 
          marginTop: '1rem',
          padding: '0.75rem',
          backgroundColor: 'var(--itak-background-tertiary)',
          borderRadius: 'var(--radius-sm)',
          fontSize: '0.9rem',
          color: 'var(--itak-text-secondary)'
        }}>
          <strong>Status:</strong> {processState.active ? '🟢 Running' : '🔴 Stopped'}
          {busyFlag && ' (Processing...)'}
        </div>
      </div>
      
      <div className="card">
        <h2 className="card-header">Execute Command</h2>
        
        <div className="input-group">
          <label className="input-label">Command</label>
          <input 
            type="text"
            className="text-input"
            placeholder="e.g., create, run, version"
            value={commandText}
            onChange={(e) => setCommandText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleRunCommand()}
          />
        </div>
        
        <div className="input-group">
          <label className="input-label">Arguments (space-separated)</label>
          <input 
            type="text"
            className="text-input"
            placeholder="e.g., --help --verbose"
            value={commandArgs}
            onChange={(e) => setCommandArgs(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleRunCommand()}
          />
        </div>
        
        <button 
          className="btn btn-primary"
          onClick={handleRunCommand}
          disabled={busyFlag || !commandText.trim()}
        >
          🚀 Execute
        </button>
      </div>
      
      <div className="card">
        <h2 className="card-header">Send Input to Agent</h2>
        
        <div className="input-group">
          <label className="input-label">Input Text</label>
          <input 
            type="text"
            className="text-input"
            placeholder="Type command or input for running agent..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendInput()}
            disabled={!processState.active}
          />
        </div>
        
        <button 
          className="btn btn-primary"
          onClick={handleSendInput}
          disabled={!processState.active || !inputText.trim()}
        >
          📤 Send
        </button>
        
        {!processState.active && (
          <div style={{ 
            marginTop: '0.75rem',
            padding: '0.5rem',
            backgroundColor: 'rgba(136, 136, 136, 0.1)',
            borderRadius: 'var(--radius-sm)',
            fontSize: '0.85rem',
            color: 'var(--itak-text-muted)'
          }}>
            ⚠️ Agent must be running to send input
          </div>
        )}
      </div>
    </div>
  );
}
