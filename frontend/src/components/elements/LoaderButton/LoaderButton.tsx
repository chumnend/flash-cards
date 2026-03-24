interface Props {
    label: string;
    loadingLabel: string;
    isLoading: boolean;
}

const SubmitButton = ({ label, loadingLabel, isLoading }: Props) => {
    return (
        <button
            type="submit"
            className="button button--primary form-submit"
            disabled={isLoading}
        >
            {isLoading ? loadingLabel : label}
        </button>
    );
};

export default SubmitButton;