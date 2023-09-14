// StarRating.js
import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faStar as solidStar } from "@fortawesome/free-solid-svg-icons";
import { faStar as emptyStar } from "@fortawesome/free-regular-svg-icons";

const StarRating = ({ totalStars, initialRating }) => {
  const [rating, setRating] = useState(initialRating || 0);

  const handleClick = (star) => {
    setRating(star);
  };

  return (
    <div>
      {[...Array(totalStars)].map((_, index) => {
        const star = index + 1;
        return (
          <span
            key={star}
            onClick={() => handleClick(star)}
            style={{ cursor: "pointer" }}
          >
            <FontAwesomeIcon
              icon={star <= rating ? solidStar : emptyStar}
              color={star <= rating ? "gold" : "gray"}
            />
          </span>
        );
      })}
    </div>
  );
};

export default StarRating;
