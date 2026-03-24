import type { InputHTMLAttributes } from 'react';

interface Props extends InputHTMLAttributes<HTMLInputElement> {
    label: string;
}

const FormField = ({ label, ...inputProps }: Props) => {
    return (
        <label className="form-field">
            <span className="form-label">{label}</span>
            <input className="form-input" {...inputProps} />
        </label>
    );
};

export default FormField;
