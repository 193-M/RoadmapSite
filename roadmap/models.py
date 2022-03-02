from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# クラスモデル
class UserClass(models.Model):
    userclass = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        verbose_name="クラス"
    )

# ユーザーモデル
class CustomUserManager(UserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=20,
        unique=False,
        verbose_name="名前"
        )
    email = models.EmailField(
        unique=True,
        verbose_name="メールアドレス"
    )
    userclass = models.ForeignKey(
        UserClass,
        on_delete=models.CASCADE,
        to_field='userclass',
        blank=True,
        null=True,
        verbose_name="クラス"
        )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="スタッフ権限"
    )
    
    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# ロードマップモデル
# 大項目(タイトル)
class RoadMapTitles(models.Model):
    title = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        verbose_name="タイトル"
    )

# 中項目(中身)
class RoadMapContents(models.Model):
    content = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        verbose_name="内容"
    )
    content_title = models.ForeignKey(RoadMapTitles, on_delete=models.CASCADE, related_name='roadmaptitle')

# 小項目(詳細)
class RoadMapIndexes(models.Model):
    index = models.CharField(
        max_length=50,
        blank=False,
        verbose_name="詳細"
    )
    index_title = models.ForeignKey(RoadMapContents, on_delete=models.CASCADE, related_name='contenttitle')