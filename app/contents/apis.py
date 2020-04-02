import random

from django.db.models import Max, Min
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from contents.models import Contents
from contents.serializers import ContentsDetailSerializer, ContentsSerializer, WatchingSerializer, \
    PreviewContentsSerializer
from members.models import Profile, Watching


def get_ad_contents():
    max_id = Contents.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        contents = Contents.objects.filter(pk=pk, preview_video__isnull=False).first()
        if contents:
            return contents


def get_top_contents():
    max_id = Contents.objects.filter(contents_pub_year='2020').aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        contents = Contents.objects.filter(pk=pk).first()
        if contents:
            return contents


def get_preview_video():
    max_id = Contents.objects.filter(preview_video__isnull=False).aggregate(max_id=Max("id"))['max_id']
    min_id = Contents.objects.filter(preview_video__isnull=False).aggregate(min_id=Min("id"))['min_id']
    video_list = []
    while True:
        if len(video_list) == 10:
            break
        else:
            pk = random.randint(min_id, max_id)
            video_list.append(pk)
    return video_list


class ContentsRetrieveListView(APIView):
    def get(self, request, profile_pk, contents_pk):
        contents = Contents.objects.get(pk=contents_pk)
        serializer = ContentsDetailSerializer(contents)
        profile = Profile.objects.get(pk=profile_pk)
        is_selected = True if profile in contents.select_profiles.all() else False
        is_like = True if profile in contents.like_profiles.all() else False
        data = {
            'contents': serializer.data,
            'is_selected': is_selected,
            'is_like': is_like,
        }
        return Response(data)


class ContentsLikeAPIView(APIView):
    def get(self, request, profile_pk, contents_pk):
        profile = Profile.objects.get(pk=profile_pk)
        contents = Contents.objects.get(pk=contents_pk)

        if profile in contents.like_profiles.all():
            contents.like_profiles.remove(profile)
        else:
            contents.like_profiles.add(profile)

        return Response(status=status.HTTP_200_OK)


class ContentsSelectAPIView(APIView):
    def get(self, request, profile_pk, contents_pk):
        profile = Profile.objects.get(pk=profile_pk)
        contents = Contents.objects.get(pk=contents_pk)

        if profile in contents.select_profiles.all():
            contents.select_profiles.remove(profile)
        else:
            contents.select_profiles.add(profile)

        return Response(status=status.HTTP_200_OK)


# class ContentsListView(generics.ListAPIView):
#     serializer_class = ContentsSerializer
#     queryset = Contents.objects.all()
#
#     def list(self, request, *args, **kwargs):
#         all_contents = self.get_queryset()
#         recommand_contents = all_contents.filter(contents_pub_year='2020')[:10]
#         top_contents = get_top_contents()
#         ad_contents = get_ad_contents()
#         preview_contents = Contents.objects.all()[:10]
#
#         serializer_all = self.get_serializer(all_contents, many=True)
#         serializer_recommand = self.get_serializer(recommand_contents, many=True)
#         serializer_preview = self.get_serializer(preview_contents, many=True)
#         serializer_top = ContentsDetailSerializer(top_contents)
#         serializer_ad = ContentsDetailSerializer(ad_contents)
#
#         data = {
#             "top_contents": serializer_top.data,
#             "ad_contents": serializer_ad.data,
#             "recommand_contents": serializer_recommand.data,
#             "preview_contents": serializer_preview.data,
#             "all_contents": serializer_all.data
#         }
#         return Response(data)
class ContentsListView(APIView):

    def get(self, request, profile_pk):
        all_contents = Contents.objects.all()
        recommand_contents = all_contents.filter(contents_pub_year='2020')[:10]
        top_contents = get_top_contents()
        ad_contents = get_ad_contents()
        preview_contents = Contents.objects.filter(pk__in=get_preview_video())
        watching_video = Watching.objects.filter(profile__id=profile_pk)

        serializer_all = ContentsSerializer(all_contents, many=True)
        serializer_recommand = ContentsSerializer(recommand_contents, many=True)
        serializer_top = ContentsDetailSerializer(top_contents)
        serializer_ad = ContentsDetailSerializer(ad_contents)
        serializer_watching_video = WatchingSerializer(watching_video, many=True)
        serializer_preview = PreviewContentsSerializer(preview_contents, many=True)

        data = {
            "top_contents": serializer_top.data,
            "ad_contents": serializer_ad.data,
            "recommand_contents": serializer_recommand.data,
            "preview_contents": serializer_preview.data,
            "all_contents": serializer_all.data,
            "watcing_video": serializer_watching_video.data
        }
        return Response(data)
