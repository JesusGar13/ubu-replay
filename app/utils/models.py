from typing import List
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Base(DeclarativeBase):   
    pass


class User(Base, UserMixin):
    """
    Modelo de usuario
    """
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    web_denegadas: Mapped[List["WebDenegadas"]] = relationship(back_populates="user")

    sessions: Mapped[List["Session"]] = relationship(back_populates="user")
    

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Session(Base):
    """
    Modelo de sesión de trackeo
    """
    __tablename__ = "session"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    time_start: Mapped[datetime] = mapped_column(nullable=False)
    time_end: Mapped[datetime] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="sessions")
    sitios_web: Mapped[List["SitioWebSession"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class SitioWeb(Base):
    """
    Modelo de sitio web a trackear
    """
    __tablename__ = "sitio_web"
    id: Mapped[int] = mapped_column(primary_key=True)
    main_url: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    webs: Mapped[List["Webs"]] = relationship(
        back_populates="sitio_web", cascade="all, delete-orphan"
    )
    sesiones: Mapped[List["SitioWebSession"]] = relationship(
        back_populates="sitio_web", cascade="all, delete-orphan"
    )
    web_denegadas: Mapped[List["WebDenegadas"]] = relationship(
        back_populates="sitio_web", cascade="all, delete-orphan"
    )


class Webs(Base):
    """
    Modelo de subpáginas web trackeadas dentro de un sitio web
    """
    __tablename__ = "webs"
    id: Mapped[int] = mapped_column(primary_key=True)
    sitio_web_id: Mapped[int] = mapped_column(ForeignKey("sitio_web.id"), nullable=False)
    url: Mapped[str] = mapped_column(String(150), nullable=False)

    sitio_web: Mapped["SitioWeb"] = relationship(back_populates="webs")


class SitioWebSession(Base):
    """
    Modelo de sesión de trackeo de sitio web
    """
    __tablename__ = "sitiowebsession"
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("session.id"), nullable=False)
    sitio_web_id: Mapped[int] = mapped_column(ForeignKey("sitio_web.id"), nullable=False)

    sitio_web: Mapped["SitioWeb"] = relationship(back_populates="sesiones")
    session: Mapped["Session"] = relationship(back_populates="sitios_web")


class WebDenegadas(Base):
    """
    Modelo de páginas web denegadas
    """
    __tablename__ = "web_denegadas"
    id: Mapped[int] = mapped_column(primary_key=True)
    sitio_web_id: Mapped[int] = mapped_column(ForeignKey("sitio_web.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    sitio_web: Mapped["SitioWeb"] = relationship(back_populates="web_denegadas")
    user: Mapped["User"] = relationship(back_populates="web_denegadas")
