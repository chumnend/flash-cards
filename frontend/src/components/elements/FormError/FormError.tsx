interface Props {
    message: string | null;
}

const FormError = ({ message }: Props) => {
    if (!message) return null;
    return <p className="form-error">{message}</p>;
};

export default FormError;
