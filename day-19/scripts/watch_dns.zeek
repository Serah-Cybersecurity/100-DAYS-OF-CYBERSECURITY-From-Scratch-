event dns_request(
    c: connection,
    msg: dns_msg,
    query: string,
    qtype: count,
    qclass: count
)
{
    if (query == "example.com")
    {
        print fmt(
            "LAB DNS QUERY: originator=%s resolver=%s query=%s qtype=%d",
            c$id$orig_h,
            c$id$resp_h,
            query,
            qtype
        );
    }
}
