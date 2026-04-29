from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Block, Room
import random
from django.core.mail import send_mail
from django.conf import settings
from .models import ExamSlot


@login_required(login_url='login')
def blocks_view(request):
    if request.method == 'POST':
        # Add block
        if 'add' in request.POST:
            name = request.POST.get('block_name')
            if name:
                Block.objects.get_or_create(name=name)

        # Delete block
        if 'delete' in request.POST:
            block_id = request.POST.get('delete')
            Block.objects.filter(id=block_id).delete()

        # Next step
        if 'next' in request.POST:
            selected = request.POST.getlist('blocks')
            request.session['selected_blocks'] = selected
            return redirect('rooms')

    blocks = Block.objects.all()
    return render(request, 'seating/blocks.html', {'blocks': blocks})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Block, Room


@login_required(login_url='login')
def rooms_view(request):
    selected_blocks = request.session.get('selected_blocks', [])

    if request.method == 'POST':

        # ➕ Add room
        if 'add' in request.POST:
            block_id = request.POST.get('block')
            room_number = request.POST.get('room_number')
            rows = request.POST.get('rows')
            columns = request.POST.get('columns')

            if block_id and room_number and rows and columns:
                Room.objects.create(
                    block_id=block_id,
                    room_number=room_number,
                    rows=int(rows),
                    columns=int(columns),
                    capacity=int(rows) * int(columns)
                )
                return redirect('rooms')

        # ❌ Delete room
        if 'delete' in request.POST:
            room_id = request.POST.get('delete')
            Room.objects.filter(id=room_id).delete()
            return redirect('rooms')

        # ➡️ Next step
        if 'next' in request.POST:
            selected_rooms = request.POST.getlist('rooms')
            request.session['selected_rooms'] = selected_rooms
            return redirect('exam_slot')

    rooms = Room.objects.filter(block__id__in=selected_blocks)
    blocks = Block.objects.filter(id__in=selected_blocks)

    return render(request, 'seating/rooms.html', {
        'rooms': rooms,
        'blocks': blocks
    })



from .models import ExamSlot


@login_required(login_url='login')
def exam_slot_view(request):
    if request.method == 'POST':
        # Add slot
        if 'add' in request.POST:
            name = request.POST.get('name')
            date = request.POST.get('date')
            time_range = request.POST.get('time_range')
            if name and date and time_range:
                ExamSlot.objects.create(
                    name=name,
                    date=date,
                    time_range=time_range
                )

        # Delete slot
        if 'delete' in request.POST:
            slot_id = request.POST.get('delete')
            ExamSlot.objects.filter(id=slot_id).delete()

        # Next step
        if 'next' in request.POST:
            slot_id = request.POST.get('slot')
            request.session['exam_slot'] = slot_id
            return redirect('upload')

    slots = ExamSlot.objects.all()
    return render(request, 'seating/exam_slot.html', {'slots': slots})



import pandas as pd
from django.core.files.storage import FileSystemStorage


@login_required(login_url='login')
def upload_view(request):
    if request.method == 'POST' and request.FILES.get('excel'):
        excel_file = request.FILES['excel']

        # Save file temporarily
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        # Read Excel
        df = pd.read_excel(file_path)

        # Convert to list of dicts and store in session
        request.session['students_data'] = df.to_dict(orient='records')

        return redirect('seating')

    return render(request, 'seating/upload.html')





def send_seat_email(student, exam_slot):
    subject = "Your Exam Seating Details"

    message = f"""
Dear {student['name']},

Your exam seating has been allocated successfully.

Subject: {student['subject']}
Room: {student['room']}
Row: {student['row']}
Column: {student['col']}

Exam Date: {exam_slot.date}
Exam Time: {exam_slot.time_range}

Please report 30 minutes early.

All the best!
Exam Cell
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [student['email']],
        fail_silently=False,
    )



import random
import csv
from django.http import HttpResponse


@login_required(login_url='login')
def seating_view(request):
    list(messages.get_messages(request)) 
    students = request.session.get('students_data', [])
    room_ids = request.session.get('selected_rooms', [])

    rooms = Room.objects.filter(id__in=room_ids)

    if not students or not rooms:
        return render(request, 'seating/seating.html', {'seat_map': {}})

    # 🔹 Group by branch
    branch_map = {}
    for s in students:
        branch = s.get('Branch')
        branch_map.setdefault(branch, []).append(s)

    # 🔹 Sort each branch by RollNo
    for b in branch_map:
        branch_map[b] = sorted(branch_map[b], key=lambda x: x.get('RollNo'))

    # 🔹 Interleave branches
    ordered_students = []
    while any(branch_map.values()):
        for b in list(branch_map.keys()):
            if branch_map[b]:
                ordered_students.append(branch_map[b].pop(0))

    seating = []
    seat_map = {}
    idx = 0

    for room in rooms:
        room_seats = []
        for row in range(1, 7):      # 6 rows
            for col in range(1, 5):  # 4 columns
                if idx < len(ordered_students):
                    s = ordered_students[idx]
                    seat = {
                        'room': f"{room.block.name}{room.room_number}",
                        'row': row,
                        'col': col,
                        'roll': s.get('RollNo'),
                        'name': s.get('Name'),
                        'email': s.get('Email'),
                        'branch': s.get('Branch'),
                        'subject': s.get('Subject')
                    }
                    room_seats.append(seat)
                    seating.append(seat)
                    idx += 1

        seat_map[f"{room.block.name}{room.room_number}"] = room_seats

    # Save seating
    request.session['final_seating'] = seating

    return render(request, 'seating/seating.html', {
        'seat_map': seat_map
    })




import pandas as pd
from django.http import HttpResponse


@login_required(login_url='login')
def download_seating(request):
    seating = request.session.get('final_seating', [])

    if not seating:
        return HttpResponse("No seating data found.", status=400)

    # Convert to DataFrame
    df = pd.DataFrame(seating)

    # Rename columns nicely
    df = df.rename(columns={
        'room': 'Room',
        'row': 'Row',
        'col': 'Column',
        'roll': 'Roll No',
        'name': 'Name',
        'email': 'Email',
        'branch': 'Branch',
        'subject': 'Subject'
    })

    # Create Excel response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=seating.xlsx'

    # Write to Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Seating')

    return response


from django.shortcuts import redirect
from django.contrib import messages

def send_mails_view(request):
    seating = request.session.get('final_seating')
    slot_id = request.session.get('exam_slot')

    if not seating or not slot_id:
        messages.error(request, "No seating data found. Please generate seating first.")
        return redirect('seating')

    exam_slot = ExamSlot.objects.get(id=slot_id)

    for s in seating:
        send_seat_email(s, exam_slot)

    messages.success(request, "Emails sent successfully to all students!")
    return redirect('seating')


@login_required(login_url='login')
def home(request):
    return render(request, 'seating/home.html')
