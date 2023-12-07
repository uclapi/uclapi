import Image from "next/image";

/**
These are the rounded icons at the end of fields. Can change everything except
how the actions are linked up

image,
description,
onClick default: null,
style default: styles.button
**/

const logosize = 20;

const Icon = ({ image = null, description = "", onClick = () => {} }) => (
  <div className="icon-wrapper" onClick={onClick}>
    {image && (
      <Image
        src={image}
        width={logosize}
        height={logosize}
        description={description}
        centred
      />
    )}
  </div>
);

export default Icon;
