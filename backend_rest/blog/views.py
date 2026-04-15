from django.db.models import Count, Prefetch
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Blog, Comment, Upvote
from .serializer import BlogSerializer, CommentSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.db.models import Count, Prefetch, Exists, OuterRef

def get_blog_queryset(user_id=None):
    comment_queryset = Comment.objects.select_related("U_ID").order_by("created_at")

    queryset = (
        Blog.objects.select_related("U_ID")
        .annotate(upvote_count=Count("upvotes"))
        .prefetch_related(Prefetch("comments", queryset=comment_queryset))
        .order_by("-id")
    )

    # 🔥 Add this
    if user_id:
        queryset = queryset.annotate(
            is_upvoted=Exists(
                Upvote.objects.filter(
                    blog=OuterRef('pk'),
                    U_ID_id=user_id
                )
            )
        )

    return queryset
# GET all blogs / POST new blog
# function-based API views
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def blog_list(request):
    user = request.user
    user_id=user.U_ID
    print(user_id)
    if request.method == "GET":
        blogs = get_blog_queryset(user_id)
        serializer = BlogSerializer(blogs, many=True)  # to json
        return Response(serializer.data)  # json->response

    elif request.method == "POST":
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET single blog / PUT update / DELETE
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def blog_detail(request, pk):
    user = request.user
    user_id=user.U_ID
    try:
        if request.method == "GET":
            blog = get_blog_queryset(user_id).get(pk=pk)
        else:
            blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["POST"])
@permission_classes([AllowAny])
def add_comment(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(data={
        **request.data,
        'blog': blog.id
    })
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_upvote(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=404)

    user = request.user   # ✅ authenticated user

    existing = Upvote.objects.filter(blog=blog, U_ID=user).first()

    if existing:
        existing.delete()
        return Response({
            "upvoted": False,
            "upvote_count": blog.upvotes.count()
        })
    else:
        Upvote.objects.create(blog=blog, U_ID=user)
        return Response({
            "upvoted": True,
            "upvote_count": blog.upvotes.count()
        })