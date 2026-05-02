import './Switch.css'

interface SwitchProps {
    isOn: boolean;
    handleToggle: () => void;
}

export function Switch({ isOn, handleToggle }: SwitchProps) {
    return (
        <label className="switch">
            <input 
                type="checkbox" 
                checked={isOn} 
                onChange={handleToggle} 
            />
            <span className="slider round" />
        </label>
    );
}