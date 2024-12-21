import React from 'react';
import clsx from 'clsx'; // Asegúrate de instalarlo: npm install clsx

export const Card = ({
  children,
  className,
  style,
}: {
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
}) => (
  <div className={clsx('p-4 rounded-lg shadow', className)} style={style}>
    {children}
  </div>
);

export const CardHeader = ({
  children,
  className,
  style,
}: {
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
}) => (
  <div className={clsx('mb-4', className)} style={style}>
    {children}
  </div>
);

export const CardTitle = ({
  children,
  className,
  style,
}: {
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
}) => (
  <h3 className={clsx('text-lg font-bold', className)} style={style}>
    {children}
  </h3>
);

export const CardContent = ({
  children,
  className,
  style,
}: {
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
}) => (
  <div className={clsx('', className)} style={style}>
    {children}
  </div>
);

const Cards = {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
};

export default Cards;
