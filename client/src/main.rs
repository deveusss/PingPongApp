use std::net::Ipv6Addr;
use std::net::SocketAddr;
use wtransport::ClientConfig;
use wtransport::Endpoint;

#[tokio::main]
async fn main() {
    let config =
        ClientConfig::builder().with_bind_address(SocketAddr::new(Ipv6Addr::UNSPECIFIED.into(), 8000));

    let connection = Endpoint::client(config)
        .unwrap()
        .connect("0.0.0.0:8000".parse().unwrap(), "localhost")
        .unwrap()
        .await
        .unwrap();
    println!("Connected!");
    let mut stream = connection.open_bi().await.unwrap();
    stream.0.write_all(b"ping").await.unwrap();
    stream.0.finish().await.unwrap();
}
