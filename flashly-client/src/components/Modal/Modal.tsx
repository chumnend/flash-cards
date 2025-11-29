import React, { useEffect } from 'react';

import './Modal.css';

export type ModalProps = {
    children: React.ReactNode;
    isOpen: boolean;
    title?: string;
    footer?: React.ReactNode;
    onClose: () => void;
};

const Modal = (props: ModalProps) => {
    const { children, isOpen,  title, footer, onClose } = props;

    useEffect(() => {
        const handleEscape = (event: KeyboardEvent) => {
            if (event.key === 'Escape') {
                onClose();
            }
        };

        if (isOpen) {
            document.addEventListener('keydown', handleEscape);
            // Prevent body scroll when modal is open
            document.body.style.overflow = 'hidden';
        }

        return () => {
            document.removeEventListener('keydown', handleEscape);
            document.body.style.overflow = 'unset';
        };
    }, [isOpen, onClose]);

    const handleBackdropClick = (event: React.MouseEvent<HTMLDivElement>) => {
        if (event.target === event.currentTarget) {
            onClose();
        }
    };

    if (!isOpen) {
        return null;
    }

    return (
        <div className="modal" onClick={handleBackdropClick}>
            <div className="modal-content">
                {title && (
                    <div className="modal-header">
                        <h2 className="modal-title">{title}</h2>
                        <button 
                            className="modal-close" 
                            onClick={onClose}
                            aria-label="Fermer"
                        >
                            ×
                        </button>
                    </div>
                )}
                <div className="modal-body">
                    {children}
                </div>
                {footer && (
                    <div className="modal-footer">
                        {footer}
                    </div>
                )}
            </div>
        </div>
    );
}

export default Modal;
