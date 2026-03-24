import { useState } from 'react';
import type { ChangeEvent, FormEvent } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';

import { useAuth } from '../../providers/AuthProvider';
import Page from '../../layout/Page';
import FormField from '../../elements/FormField';
import FormError from '../../elements/FormError';
import LoaderButton from '../../elements/LoaderButton';

const LoginPage = () => {
    const auth = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    const [formValues, setFormValues] = useState({ email: '', password: '' });
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target;
        setFormValues((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (isSubmitting) return;

        setError(null);
        setIsSubmitting(true);

        try {
            await auth.login({ email: formValues.email.trim(), password: formValues.password });
            const from = location.state?.from?.pathname ?? '/feed';
            navigate(from, { replace: true });
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
                    <h1 className="page-title">Login</h1>
                    <p className="page-subtitle">Welcome back. Enter your details to continue.</p>
                </header>

                <form className="form" onSubmit={handleSubmit}>
                    <FormField
                        label="Email"
                        type="email"
                        name="email"
                        placeholder="you@example.com"
                        autoComplete="email"
                        value={formValues.email}
                        onChange={handleChange}
                        required
                    />
                    <FormField
                        label="Password"
                        type="password"
                        name="password"
                        placeholder="••••••••"
                        autoComplete="current-password"
                        value={formValues.password}
                        onChange={handleChange}
                        required
                    />
                    <FormError message={error} />
                    <LoaderButton label="Login" loadingLabel="Logging in..." isLoading={isSubmitting} />
                </form>

                <p className="page-footer-text">
                    New here? <Link to="/register">Create an account</Link>
                </p>
                <p className="page-footer-text">
                    <Link to="/">Back to home</Link>
                </p>
            </section>
        </Page>
    );
};

export default LoginPage;
