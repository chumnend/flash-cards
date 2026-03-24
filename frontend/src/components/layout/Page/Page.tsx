import type React from "react"

import './Page.css'

type Props = {
    children: React.ReactNode,
}

const Page = ({ children }: Props) => {
    return (
        <div className="page">
            {children}
        </div>
    )
}

export default Page;
