import { useRouter } from "next/router";
import { allApps } from "@/data/app_pages.jsx";
import { CardView, Container, Row } from "@/components/layout/Items.jsx";
import { Button } from "rsuite";
import React from "react";
import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";

import Image from "next/image";
import styles from "@/styles/MarketplaceAppPage.module.scss";
import Head from "next/head";

export async function getStaticPaths() {
  return {
    paths: Object.keys(allApps).map((app) => ({ params: { app } })),
    fallback: false,
  };
}

export async function getStaticProps(context) {
  return { props: { appId: context.params.app } };
}

export default function MarketplaceApp() {
  const router = useRouter();
  const { app:appId } = router.query;
  const app = allApps[appId];
  const {
    logodark,
    name,
    description,
    screenshots,
    detailedDescription,
    links,
  } = app

  return (
    <>
      <Head>
        <title>
          {name} - UCL API Marketplace
        </title>
      </Head>

      <Container styling="splash-parallax" style={{ margin: `60px 0 0 0` }}>
        <div className={styles.appWrapper}>
          <div className={styles.titleWrapper}>
            <Image
              className={styles.logo}
              src={logodark}
              width={100}
              height={100}
            />
            <div>
              <h2>{name}</h2>
              <p>{description}</p>
            </div>
            <div className={styles.links}>
              {links.map((x, key) => (
                <Container height="50px" noPadding key={key}>
                  <Row width="2-3" horizontalAlignment="center">
                    <Button href={x.link} key={key} style={{ width: `100px` }}>
                      {x.name}
                    </Button>
                  </Row>
                </Container>
              ))}
            </div>
          </div>

          <CardView width="1-1" noPadding style={{ padding: `20px 0` }}>
            <div className={styles.carouselWrapper}>
              <Carousel
                responsive={{
                  desktop: {
                    breakpoint: { max: 3000, min: 1024 },
                    items: 3,
                  },
                  tablet: {
                    breakpoint: { max: 1024, min: 464 },
                    items: 2,
                  },
                  mobile: {
                    breakpoint: { max: 464, min: 0 },
                    items: 1,
                  },
                }}
                infinite
                showDots
              >
                {screenshots.map((screenshot) => (
                  <div key={screenshot.img}>
                    <img src={screenshot.img} width={"100%"} />
                    <p className="legend">{screenshot.name}</p>
                  </div>
                ))}
              </Carousel>
            </div>

            <div className={styles.description}>{detailedDescription}</div>
          </CardView>
        </div>
      </Container>
    </>
  );
}
