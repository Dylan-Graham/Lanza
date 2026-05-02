import './Switch.css'

interface SwitchProps {
    isOn: boolean;
    handleToggle: () => void;
}

export function Switch({ isOn, handleToggle }: SwitchProps) {
    return (
        <div className="switch-container">
            <label className="switch">
                <input
                    type="checkbox"
                    checked={isOn}
                    onChange={handleToggle}
                />
                <span className="slider round">
                    <div className="slider-thumb"></div>
                </span>
            </label>
        </div>
    );
}