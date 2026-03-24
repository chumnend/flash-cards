import { useState } from 'react';
import type { ChangeEvent, FormEvent } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { registerUser } from '../../../helpers/api/auth';
import { useAuth } from '../../providers/AuthProvider';
import Page from '../../layout/Page';
import FormField from '../../elements/FormField';
import FormError from '../../elements/FormError';
import LoaderButton from '../../elements/LoaderButton';

const RegisterPage = () => {
    const auth = useAuth();
    const navigate = useNavigate();

    const [formValues, setFormValues] = useState({
        firstName: '',
        lastName: '',
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
    });
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target;
        setFormValues((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (isSubmitting) return;

        const { firstName, lastName, username, email, password, confirmPassword } = formValues;

        if (password !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        setError(null);
        setIsSubmitting(true);

        try {
            await registerUser({ firstName: firstName.trim(), lastName: lastName.trim(), username: username.trim(), email: email.trim(), password });
            await auth.login({ email: email.trim(), password });
            navigate('/feed');
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Something went wrong. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <Page>
            <section className="page-card">
                <header className="page-header">
                    <h1 className="page-title">Create your account</h1>
                    <p className="page-subtitle">Start building decks in a few seconds.</p>
                </header>

                <form className="form" onSubmit={handleSubmit}>
                    <FormField label="First name" type="text" name="firstName" placeholder="Jane" autoComplete="given-name" value={formValues.firstName} onChange={handleChange} required />
                    <FormField label="Last name" type="text" name="lastName" placeholder="Doe" autoComplete="family-name" value={formValues.lastName} onChange={handleChange} required />
                    <FormField label="Username" type="text" name="username" placeholder="flashlyfan" autoComplete="username" value={formValues.username} onChange={handleChange} required />
                    <FormField label="Email" type="email" name="email" placeholder="you@example.com" autoComplete="email" value={formValues.email} onChange={handleChange} required />
                    <FormField label="Password" type="password" name="password" placeholder="Create a password" autoComplete="new-password" value={formValues.password} onChange={handleChange} required />
                    <FormField label="Confirm password" type="password" name="confirmPassword" placeholder="Repeat your password" autoComplete="new-password" value={formValues.confirmPassword} onChange={handleChange} required />
                    <FormError message={error} />
                    <LoaderButton label="Create account" loadingLabel="Creating account..." isLoading={isSubmitting} />
                </form>

                <p className="page-footer-text">
                    Already have an account? <Link to="/login">Login</Link>
                </p>
                <p className="page-footer-text">
                    <Link to="/">Back to home</Link>
                </p>
            </section>
        </Page>
    );
};

export default RegisterPage;