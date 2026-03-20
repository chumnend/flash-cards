import type React from "react"

type Props = {
    children: React.ReactNode,
}

const Page = (props: Props) => {
    return (
        <main className="page">
            {props.children}
        </main>
    )
}

export default Page;
