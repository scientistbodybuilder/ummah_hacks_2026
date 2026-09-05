import {
  Pagination,
  PaginationContent,
//   PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination"
import { useMemo, useState } from 'react'
import ClauseCard from "./ClauseCard"
import type {ClauseCardProps} from './ClauseCard'



const ClauseBreakdown = ({ data, file }: { data: Record<string, ClauseCardProps[]>; file: string }) => {
    const [page, setPage] = useState(1)
    const pageSize = 4
    const [ruling, setRuling] = useState(Object.keys(data)[0])
    const visibleClauses = useMemo(() => {
        const start = (page - 1) * pageSize
        return data[ruling]?.slice(start, start + pageSize) || []
    }, [data, page, ruling])
    const pageCount = Math.ceil((data[ruling]?.length || 0) / pageSize)

    return (
        <section className="w-full max-w-[1100px] scroll-mt-20 flex flex-col items-center justify-start">

            <div className="w-full flex items-center justify-end">
                <div className="rounded-[36px] border-muted-foreground bg-(--background-dark) p-1 w-auto mb-6">
                    {Object.keys(data).map((key) => (
                        <button
                            key={key}
                            className={`px-3 py-1 font-medium rounded-[36px] text-sm transform transition cursor-pointer ${ruling === key ? "bg-white text-black" : "text-muted-foreground"}`}
                            onClick={() => {
                                setRuling(key)
                                setPage(1)
                            }}
                        >
                            {key}
                        </button>
                    ))}
                </div>
            </div>

            <h3 className="text-(--accent-color) text-sm font-bold mb-4">Analysis of {file}</h3>

            <div className="grid w-full grid-cols-1 gap-5 sm:grid-cols-2">
                {visibleClauses?.map((clause) => <ClauseCard {...clause} />)}
            </div>

            {pageCount > 1 && (
                <Pagination className="mt-7">
                    <PaginationContent>
                        <PaginationItem>
                            <PaginationPrevious
                                href="#seminar-library"
                                aria-disabled={page === 1}
                                className={page === 1 ? "pointer-events-none opacity-40" : undefined}
                                onClick={(event) => {
                                    event.preventDefault();
                                    if (page > 1) setPage((current) => current - 1);
                                }}
                            />
                        </PaginationItem>
                        {Array.from({ length: pageCount }, (_, index) => {
                            const pageNumber = index + 1;
                            return (
                                <PaginationItem key={pageNumber}>
                                    <PaginationLink
                                        href="#seminar-library"
                                        isActive={page === pageNumber}
                                        onClick={(event) => {
                                            event.preventDefault();
                                            setPage(pageNumber);
                                        }}
                                    >
                                        {pageNumber}
                                    </PaginationLink>
                                </PaginationItem>
                            );
                        })}
                        <PaginationItem>
                            <PaginationNext
                                href="#seminar-library"
                                aria-disabled={page === pageCount}
                                className={page === pageCount ? "pointer-events-none opacity-40" : undefined}
                                onClick={(event) => {
                                    event.preventDefault();
                                    if (page < pageCount) setPage((current) => current + 1);
                                }}
                            />
                        </PaginationItem>
                    </PaginationContent>
                </Pagination>
            )}

        </section>
    )
}

export default ClauseBreakdown