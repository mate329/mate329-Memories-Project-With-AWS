'use client'
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Loader2 } from 'lucide-react';
import { toast } from "react-toastify";
import { useSession } from "next-auth/react";
import { useState, ChangeEvent, FormEvent } from "react";
import { createPost } from "@/services/postService";

interface FormData {
  title: string;
  description: string;
  file: File | null;
  fileBase64: string;
}

export default function SideMenu() {
  const [isLoading, setIsLoading] = useState(false);
  const { data: session } = useSession();
  const [formData, setFormData] = useState<FormData>({
    title: "",
    description: "",
    file: null,
    fileBase64: "",
  });

  const handleChange = (e: ChangeEvent<HTMLInputElement> | ChangeEvent<HTMLTextAreaElement>) => {
    const { id, value, files } = e.target as HTMLInputElement;
    if (files) {
      const file = files[0];
      if (file && file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onloadend = () => {
          setFormData((prevData) => ({
            ...prevData,
            file,
            fileBase64: reader.result as string,
          }));
        };
        reader.readAsDataURL(file);
      }
    } else {
      setFormData((prevData) => ({
        ...prevData,
        [id]: value,
      }));
    }
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    setIsLoading(true);
    e.preventDefault();
    console.log({
      title: formData.title,
      description: formData.description,
      fileBase64: formData.fileBase64
        .replace("data:image/png;base64,", "")
        .replace("data:image/jpeg;base64,", ""),
    });

    try{
      createPost({
        title: formData.title,
        description: formData.description,
        creator: session?.user?.email.split("@")[0] || "",
        image: formData.fileBase64
          .replace("data:image/png;base64,", "")
          .replace("data:image/jpeg;base64,", ""),
      });
      toast.success("Moment posted!", {
        position: 'bottom-right'
      });
      handleClearFile();
    }catch(err){
      toast.error("Failed to post moment", {
        position: 'bottom-right'
      });
    }

    setIsLoading(false);
  };

  const handleClearFile = () => {
    setFormData({
      title: "",
      description: "",
      file: null,
      fileBase64: "",
    })
  }

  return (
    <Card className="w-[350px] h-[400px] m-5">
      <CardHeader className="items-center">
        <CardTitle>Welcome {session?.user?.username}</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit}>
          <div className="grid w-full items-center gap-4">
            <div className="flex flex-col space-y-1.5">
              <Label>Post Title</Label>
              <Input onChange={handleChange} value={formData.title} id='title' placeholder="Title of your memory" />
            </div>
            <div className="flex flex-col space-y-1.5">
              <Label>Description</Label>
              <Textarea onChange={handleChange} value={formData.description} id='description' placeholder="Describe your memory!" />
            </div>
            <div className="flex flex-col space-y-1.5">
              <Label>Upload File</Label>
              <Input
                id='file'
                className='col-span-3'
                type='file'
                accept='image/*'
                onChange={handleChange}
              />
            </div>
          </div>
          <div className="flex justify-between mt-5">
            <Button variant="outline" type="button" onClick={handleClearFile}>Clear fields</Button>
            <Button type="submit">
              {isLoading ? (
                <>
                  <Loader2 size={20} className="animate-spin" /> &nbsp;
                  Posting...
                </>
              ): 
              ('Post Moment!')
            }
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}
