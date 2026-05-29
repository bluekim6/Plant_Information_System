interface StatusBlockProps {
  children: string;
  variant?: "default" | "error";
}

function StatusBlock({ children, variant = "default" }: StatusBlockProps) {
  const className =
    variant === "error"
      ? "status-block status-block--error"
      : "status-block";

  return <div className={className}>{children}</div>;
}

export default StatusBlock;
